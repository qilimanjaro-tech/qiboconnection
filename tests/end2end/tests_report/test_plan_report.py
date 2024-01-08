import argparse
import glob
import importlib
import inspect
import json
import logging
import logging.config
import os
import re
import sys

# It should be nicer to get this info from pytest but I have not find an easy ENum with all the
# possible outcomes
ALL_OUTCOMES = ["passed", "skipped", "failed"]


class MyArgumentFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass


# Utilities
def _group(values, keyField, allowDuplicates=True, keyRequired=True):
    """Given a list of maps, return a map with the elements grouped by a certain key."""
    data = {}
    for item in values:
        keyValue = item
        if callable(keyField):
            keyValue = keyField(item)
        else:
            # Allow keyField as fields.issuetype.name
            for v in keyField.split("."):
                if v not in keyValue:
                    if keyRequired:
                        raise Exception("Key %s not found in %s and it is required", v, keyValue)
                    else:
                        keyValue = None
                        break
                keyValue = keyValue[v]

        if keyValue:
            keyValue = str(keyValue)
            if allowDuplicates:
                if keyValue not in data:
                    data[keyValue] = []
                data[keyValue].append(item)
            else:
                if keyValue in data:
                    raise Exception(f"Dupplicated key {keyValue} in {data} and they are not allowed")
                data[keyValue] = item

    return data


def get_test_functions(module):
    """Get all the test functions in a given module.
    Args:
        module: module to search for tests

    Returns:
        List[any]: an array with the functions
    """
    test_functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and name.startswith("test_"):
            test_functions.append(obj)
    return test_functions


def extract_docstring(func, skip_args=True) -> str:
    """Given a function, return its docstring

    Args:
        func (_type_): the function to extract the docstring from
        skip_args (bool, optional): If True, do not the info of the function's arguments. Defaults to True.

    Returns:
        str: the docstring of the function
    """
    docstring = inspect.getdoc(func)
    if skip_args and docstring:
        docstring = re.sub(r"Args:.*", "", docstring, flags=re.DOTALL)

    return docstring if docstring else ""


def discover_tests(directory):
    """Returns an array of dictionaries with all the tests found.

    The dictionary has the following structure:
        { "name" : "name of the test", "docstring" : "docstring of the test" }

    Args:
        directory (string): the base directory with all the test files

    Returns:
        _type_: _description_
    """
    test_files = glob.glob(os.path.join(directory, "**", "test_*.py"), recursive=True)
    tests = []
    # test_files is something like: ./src/end2end/tests/test_end2end.py
    for test_file in test_files:
        # module_path is something like: ..src.end2end.tests.test_end2end
        module_path = os.path.splitext(test_file)[0]
        module_path = module_path.replace(os.sep, ".")

        # module_name is something like: .src.end2end.tests.test_end2end
        module_name = module_path.split(".", maxsplit=1)[1]

        spec = importlib.util.spec_from_file_location(module_name, test_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        # At this point, when
        #   module_name: .src.end2end.tests.test_end2end
        # when spec.loader.exec_module(module) is executed, then some code is executed
        #   [qibo-connection] 0.9.0|INFO|2023-05-23 10:53:48]: Storing personal qibo configuration...
        #   (repeated 8 times)
        # probably when importing some modules
        spec.loader.exec_module(module)

        test_functions = get_test_functions(module)
        for func in test_functions:
            test_name = func.__name__
            docstring = extract_docstring(func)
            tests.append({"file": test_file, "name": test_name, "docstring": docstring})

    return tests


def gen_test_plan(directory, file_out):
    """Create a report with the tests in the given directory.

    Args:
        directory (str): the directory where look for the tests
        file_out (str): the file with the report
    """
    logger = logging.getLogger(__name__)

    logger.info(f"Generating the json {file_out} with the test plan ... ")

    sys.path.append(directory)
    tests = discover_tests(directory)
    with open(file_out, "w") as fp:
        json.dump(tests, fp, indent=2)

    logger.info(f"File {file_out} created!")

    print(f"Report created at {file_out}")


def gen_test_run(in_json_plan: str, in_json_results: str, out_json_run: str):
    """Generates a JSON with the combination of Test Plan + Test Results

    Arguments:
        in_json_plan (str): json with the test plan
        in_json_results  (str): json with the results of running pytest
        out_json_run (str): json where a combination of in_json_plan and in_json_results,
                            so we have the info for nice reports.
    """

    logger = logging.getLogger(__name__)
    logger.info(
        f"Generating test_run: {out_json_run} using test_plan: {in_json_plan} and test_results: {in_json_results} ..."
    )

    data_test_run: dict = {"detail": {}}
    with open(in_json_plan, "r") as fp_plan:
        data_plan: dict = json.load(fp_plan)
        tests_def_by_name = _group(data_plan, "name", False)
        with open(in_json_results, "r") as fp_results:
            data_results: dict = json.load(fp_results)

            # Here the "name" is something like
            #     src/end2end/tests/test_end2end.py::test_device_selection[device0]
            # that is a comgination of
            #     file + test_name + arguments
            # From here we want to extract the test_name so we can compare with the test_names
            # defined in data_plan. Extract the test_name from the expresion cold be done
            # using regex or, as in this case, with a couple of splits
            tests_results_by_name = _group(
                values=data_results["report"]["tests"],
                keyField=lambda item: item["name"].split(":")[2].split("[")[0],
                allowDuplicates=True,
            )

            tot_test_plan = 0
            tot_test_plan_executed = 0
            tot_outcomes = {outcome: 0 for outcome in ALL_OUTCOMES}

            # Loop over all the test cases defined
            for test_name, test_info in tests_def_by_name.items():
                tot_test_plan += 1
                data_test_run["detail"][test_name] = {
                    "info": test_info,
                    "executions": 0,
                    "results": {outcome: 0 for outcome in ALL_OUTCOMES},
                }

                # Test Case executed, several runs can be performed (eg. for several devices)
                if test_name in tests_results_by_name:
                    tot_test_plan_executed += 1
                    data_test_run["detail"][test_name]["executions"] = len(tests_results_by_name[test_name])
                    for test_result in tests_results_by_name[test_name]:
                        if test_result["outcome"] not in ALL_OUTCOMES:
                            raise Exception(f"Unknown outcome in {test_result} when the exepected are {ALL_OUTCOMES}")
                        data_test_run["detail"][test_name]["results"][test_result["outcome"]] += 1
                        tot_outcomes[test_result["outcome"]] += 1
                # Test Case not executed
                else:
                    logger.warn(f"Test {test_name} defined but not performed")

    data_test_run["summary"] = {
        "tot_test_plan": tot_test_plan,
        "tot_test_plan_executed": tot_test_plan_executed,
        "tot_outcomes": tot_outcomes,
        "date_run_tests": data_results["report"]["created_at"],
    }

    with open(out_json_run, "w") as fp_run:
        json.dump(data_test_run, fp_run, indent=2)
        logger.info(f"File {out_json_run} created!")


def gen_test_run_report(out_report, tmpl_report, in_json_run):
    """Generates a HTML file with the results of the Test Run.

    Arguments:
        out_report (str): the file name with the HTML
        tmpl_report (str): the template file to generate the HTML
        in_json_run (str): the file with the test run data
    """
    is_html = out_report.endswith(".html")

    logger = logging.getLogger(__name__)

    vars = {}
    with open(in_json_run, "r") as fp_in:
        data: dict = json.load(fp_in)

        # Sumary
        vars.update({f"tot_{outcome}": 0 for outcome in ALL_OUTCOMES})
        for key, val in data["summary"].items():
            if key == "tot_outcomes":
                for outcome_name, outcome_value in val.items():
                    vars[f"tot_{outcome_name}"] = str(outcome_value)
            else:
                vars[key] = str(val)

        # Detail

        # Body: the tests
        tbody = ""
        for name, info in data["detail"].items():
            if is_html:
                tbody += "<tr>"
                tbody += f"<td>{name}</td>"
                tbody += f"<td>{info['info']['docstring']}</td>"
                for outcome in ALL_OUTCOMES:
                    tbody += f"<td>{0 if not outcome in info['results'] else info['results'][outcome]}</td>"
                tbody += "</tr>"
            else:
                docstring = info["info"]["docstring"].replace("\n", "")
                tbody += f"|{name}|{docstring}|"
                for outcome in ALL_OUTCOMES:
                    tbody += f"{0 if not outcome in info['results'] else info['results'][outcome]}|"
                tbody += "\n"
        vars["tbody"] = tbody

    with open(tmpl_report, "r") as fp_tmpl:
        html_txt = fp_tmpl.read()
        for name, value in vars.items():
            logger.info(f"Replacing {name} ...")
            html_txt = html_txt.replace(f"#{name}#", value)

        with open(out_report, "w") as fp_out:
            fp_out.write(html_txt)
            logger.info(f"File {out_report} generated!")


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=MyArgumentFormatter,
        description="""
Tools to perform several kind of reports in relation with the test definition and the test execution.
""",
    )

    parser.add_argument("--test_plan", action="store_true", help="Generates a JSON with the test plan")
    parser.add_argument(
        "--test_run", action="store_true", help="Generates a JSON that combines the test_plan and the test_execution"
    )
    parser.add_argument("--report", action="store_true", help="Generates a Report with the Test Run")

    parser.add_argument("--cfg_logger", default="./logging.ini", help="Logger config file")
    parser.add_argument("--dir", default="end2end", help="Base folder searching for tests")
    parser.add_argument("--json_plan", default="end2end/logs/test_plan.json", help="File with the report")
    parser.add_argument(
        "--json_results", default="end2end/logs/test_results.json", help="File with the result of the execution"
    )
    parser.add_argument(
        "--json_run", default="end2end/logs/test_run.json", help="File with the combination of test plan + test results"
    )
    parser.add_argument("--out_report", default="end2end/logs/test_run.html", help="HTML file with the test run")
    parser.add_argument(
        "--tmpl_report", default="end2end/tests_report/test_run.html.tmpl", help="Template with the HTML"
    )

    args = parser.parse_args()
    # logging.config.fileConfig(args.cfg_logger)

    if args.test_plan:
        gen_test_plan(args.dir, args.json_plan)
    elif args.test_run:
        gen_test_run(args.json_plan, args.json_results, args.json_run)
    elif args.report:
        gen_test_run_report(args.out_report, args.tmpl_report, args.json_run)
