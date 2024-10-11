"""Tests methods for job result"""

import numpy as np

from qiboconnection.models.job_result import JobResult
from qiboconnection.typings.enums import JobType


def test_job_result_creation():
    """Test job result creation"""
    job_result = JobResult(
        job_id=1,
        http_response="gASVsAAAAAAAAACMFW51bXB5LmNvcmUubXVsdGlhcnJheZSMDF9yZWNvbnN0cnVjdJSTlIwFbnVtcHmUjAduZGFycmF5lJOUSwCFlEMBYpSHlFKUKEsBSwWFlGgDjAVkdHlwZZSTlIwCZjiUiYiHlFKUKEsDjAE8lE5OTkr_____Sv____9LAHSUYolDKAAAAAAAAPA_AAAAAAAA8D8AAAAAAADwPwAAAAAAAPA_AAAAAAAA8D-UdJRiLg==",
        job_type=JobType.CIRCUIT,
    )

    assert isinstance(job_result, JobResult)
    assert job_result.job_id == 1
    assert (
        job_result.http_response
        == "gASVsAAAAAAAAACMFW51bXB5LmNvcmUubXVsdGlhcnJheZSMDF9yZWNvbnN0cnVjdJSTlIwFbnVtcHmUjAduZGFycmF5lJOUSwCFlEMBYpSHlFKUKEsBSwWFlGgDjAVkdHlwZZSTlIwCZjiUiYiHlFKUKEsDjAE8lE5OTkr_____Sv____9LAHSUYolDKAAAAAAAAPA_AAAAAAAA8D8AAAAAAADwPwAAAAAAAPA_AAAAAAAA8D-UdJRiLg=="
    )
    assert (job_result.data == np.array([1.0, 1.0, 1.0, 1.0, 1.0])).all()


def test_job_result_qprogram_works():
    """Test QProgrom results are returned as dicts"""

    job_result = JobResult(
        job_id=0,
        http_response="eyJ0eXBlIjogIlFQcm9ncmFtIiwgImF0dHJpYnV0ZXMiOiB7Il9ib2R5IjogeyJ0eXBlIjogIkJsb2NrIiwgImF0dHJpYnV0ZXMiOiB7Il91dWlkIjogeyJ0eXBlIjogIlVVSUQiLCAidXVpZCI6ICI2YmNlYjQ1MS0wZWUxLTQ1N2MtYTE1Ny1iMmYyZDUzOGZmYjUifSwgImVsZW1lbnRzIjogeyJ0eXBlIjogImxpc3QiLCAiZWxlbWVudHMiOiBbeyJ0eXBlIjogIkF2ZXJhZ2UiLCAiYXR0cmlidXRlcyI6IHsiX3V1aWQiOiB7InR5cGUiOiAiVVVJRCIsICJ1dWlkIjogIjIwM2MzY2U2LTVjNzktNGQwZS1iMzYzLTgyZDQ4NDgwYWI5OCJ9LCAiZWxlbWVudHMiOiB7InR5cGUiOiAibGlzdCIsICJlbGVtZW50cyI6IFt7InR5cGUiOiAiRm9yTG9vcCIsICJhdHRyaWJ1dGVzIjogeyJfdXVpZCI6IHsidHlwZSI6ICJVVUlEIiwgInV1aWQiOiAiYzhkNjYzMzgtYzU0OS00MjcwLWI0NjAtNjA4NmE0OTE0ODMzIn0sICJlbGVtZW50cyI6IHsidHlwZSI6ICJsaXN0IiwgImVsZW1lbnRzIjogW3sidHlwZSI6ICJTZXRHYWluIiwgImF0dHJpYnV0ZXMiOiB7Il91dWlkIjogeyJ0eXBlIjogIlVVSUQiLCAidXVpZCI6ICJmZGFkMjAwOC1iODViLTRiYjYtYjIwYi1jZjQ2NmQxZGFlNTgifSwgImJ1cyI6ICJkcml2ZV9xMF9idXMiLCAiZ2FpbiI6IHsidHlwZSI6ICJGbG9hdFZhcmlhYmxlIiwgImF0dHJpYnV0ZXMiOiB7Il91dWlkIjogeyJ0eXBlIjogIlVVSUQiLCAidXVpZCI6ICI2MzVkZjdjYS1jZTM4LTRkNjItOWZlZC03ZjFjYmFmNzFlNzkifSwgIl9zb3VyY2UiOiB7InR5cGUiOiAiVmFsdWVTb3VyY2UiLCAiYXR0cmlidXRlcyI6IHsidmFsdWUiOiAiRnJlZSJ9fSwgIl92YWx1ZSI6IG51bGwsICJfZG9tYWluIjogeyJ0eXBlIjogIkRvbWFpbiIsICJhdHRyaWJ1dGVzIjogeyJ2YWx1ZSI6ICJWb2x0YWdlIn19fX19fSwgeyJ0eXBlIjogIlBsYXkiLCAiYXR0cmlidXRlcyI6IHsiX3V1aWQiOiB7InR5cGUiOiAiVVVJRCIsICJ1dWlkIjogImFiY2FjZDExLWU0YWEtNDI5Yi1iNjNjLTNhMjUwOWJjYTE3ZiJ9LCAiYnVzIjogImRyaXZlX3EwX2J1cyIsICJ3YXZlZm9ybSI6IHsidHlwZSI6ICJJUVBhaXIiLCAiYXR0cmlidXRlcyI6IHsiSSI6IHsidHlwZSI6ICJHYXVzc2lhbiIsICJhdHRyaWJ1dGVzIjogeyJhbXBsaXR1ZGUiOiAxLjAsICJkdXJhdGlvbiI6IDQwLCAibnVtX3NpZ21hcyI6IDQuNX19LCAiUSI6IHsidHlwZSI6ICJEcmFnQ29ycmVjdGlvbiIsICJhdHRyaWJ1dGVzIjogeyJkcmFnX2NvZWZmaWNpZW50IjogLTIuMCwgIndhdmVmb3JtIjogeyJ0eXBlIjogIkdhdXNzaWFuIiwgImF0dHJpYnV0ZXMiOiB7ImFtcGxpdHVkZSI6IDEuMCwgImR1cmF0aW9uIjogNDAsICJudW1fc2lnbWFzIjogNC41fX19fX19LCAid2FpdF90aW1lIjogbnVsbH19LCB7InR5cGUiOiAiU3luYyIsICJhdHRyaWJ1dGVzIjogeyJfdXVpZCI6IHsidHlwZSI6ICJVVUlEIiwgInV1aWQiOiAiOWRhZDJhYzYtYzk1OC00Y2Q5LTg1MzItMmMyMzJhNTJkMzg3In0sICJidXNlcyI6IG51bGx9fSwgeyJ0eXBlIjogIlBsYXkiLCAiYXR0cmlidXRlcyI6IHsiX3V1aWQiOiB7InR5cGUiOiAiVVVJRCIsICJ1dWlkIjogIjRlMmEzYTc1LWJkYzEtNDEzZi04ZDg1LTY3MDM5NThkMzg3NSJ9LCAiYnVzIjogInJlYWRvdXRfcTBfYnVzIiwgIndhdmVmb3JtIjogeyJ0eXBlIjogIklRUGFpciIsICJhdHRyaWJ1dGVzIjogeyJJIjogeyJ0eXBlIjogIlNxdWFyZSIsICJhdHRyaWJ1dGVzIjogeyJhbXBsaXR1ZGUiOiAxLjAsICJkdXJhdGlvbiI6IDIwMDB9fSwgIlEiOiB7InR5cGUiOiAiU3F1YXJlIiwgImF0dHJpYnV0ZXMiOiB7ImFtcGxpdHVkZSI6IDAuMCwgImR1cmF0aW9uIjogMjAwMH19fX0sICJ3YWl0X3RpbWUiOiA0MH19LCB7InR5cGUiOiAiQWNxdWlyZSIsICJhdHRyaWJ1dGVzIjogeyJfdXVpZCI6IHsidHlwZSI6ICJVVUlEIiwgInV1aWQiOiAiM2Y2YmNhYjctOTJlOS00M2I4LTg5YjAtOTNiNDcxMDNjNDlhIn0sICJidXMiOiAicmVhZG91dF9xMF9idXMiLCAid2VpZ2h0cyI6IHsidHlwZSI6ICJJUVBhaXIiLCAiYXR0cmlidXRlcyI6IHsiSSI6IHsidHlwZSI6ICJTcXVhcmUiLCAiYXR0cmlidXRlcyI6IHsiYW1wbGl0dWRlIjogMS4wLCAiZHVyYXRpb24iOiAyMDAwfX0sICJRIjogeyJ0eXBlIjogIlNxdWFyZSIsICJhdHRyaWJ1dGVzIjogeyJhbXBsaXR1ZGUiOiAxLjAsICJkdXJhdGlvbiI6IDIwMDB9fX19LCAibmFtZSI6IG51bGx9fSwgeyJ0eXBlIjogIldhaXQiLCAiYXR0cmlidXRlcyI6IHsiX3V1aWQiOiB7InR5cGUiOiAiVVVJRCIsICJ1dWlkIjogIjMzNTQzMDdlLWU0OTUtNDNhMy1hODI1LTE5ZGEzZTcxMTA0ZSJ9LCAiYnVzIjogInJlYWRvdXRfcTBfYnVzIiwgImR1cmF0aW9uIjogMTAwMDB9fV19LCAidmFyaWFibGUiOiB7InR5cGUiOiAiRmxvYXRWYXJpYWJsZSIsICJhdHRyaWJ1dGVzIjogeyJfdXVpZCI6IHsidHlwZSI6ICJVVUlEIiwgInV1aWQiOiAiNjM1ZGY3Y2EtY2UzOC00ZDYyLTlmZWQtN2YxY2JhZjcxZTc5In0sICJfc291cmNlIjogeyJ0eXBlIjogIlZhbHVlU291cmNlIiwgImF0dHJpYnV0ZXMiOiB7InZhbHVlIjogIkZyZWUifX0sICJfdmFsdWUiOiBudWxsLCAiX2RvbWFpbiI6IHsidHlwZSI6ICJEb21haW4iLCAiYXR0cmlidXRlcyI6IHsidmFsdWUiOiAiVm9sdGFnZSJ9fX19LCAic3RhcnQiOiAwLjAsICJzdG9wIjogMS4wLCAic3RlcCI6IDAuMX19XX0sICJzaG90cyI6IDEwMDB9fV19fX0sICJfYnVzZXMiOiB7InR5cGUiOiAic2V0IiwgImVsZW1lbnRzIjogWyJyZWFkb3V0X3EwX2J1cyIsICJkcml2ZV9xMF9idXMiXX0sICJfdmFyaWFibGVzIjogeyJ0eXBlIjogImxpc3QiLCAiZWxlbWVudHMiOiBbeyJ0eXBlIjogIkZsb2F0VmFyaWFibGUiLCAiYXR0cmlidXRlcyI6IHsiX3V1aWQiOiB7InR5cGUiOiAiVVVJRCIsICJ1dWlkIjogIjYzNWRmN2NhLWNlMzgtNGQ2Mi05ZmVkLTdmMWNiYWY3MWU3OSJ9LCAiX3NvdXJjZSI6IHsidHlwZSI6ICJWYWx1ZVNvdXJjZSIsICJhdHRyaWJ1dGVzIjogeyJ2YWx1ZSI6ICJGcmVlIn19LCAiX3ZhbHVlIjogbnVsbCwgIl9kb21haW4iOiB7InR5cGUiOiAiRG9tYWluIiwgImF0dHJpYnV0ZXMiOiB7InZhbHVlIjogIlZvbHRhZ2UifX19fV19LCAiX2Jsb2NrX3N0YWNrIjogeyJ0eXBlIjogImRlcXVlIiwgImVsZW1lbnRzIjogW3sidHlwZSI6ICJCbG9jayIsICJhdHRyaWJ1dGVzIjogeyJfdXVpZCI6IHsidHlwZSI6ICJVVUlEIiwgInV1aWQiOiAiNmJjZWI0NTEtMGVlMS00NTdjLWExNTctYjJmMmQ1MzhmZmI1In0sICJlbGVtZW50cyI6IHsidHlwZSI6ICJsaXN0IiwgImVsZW1lbnRzIjogW3sidHlwZSI6ICJBdmVyYWdlIiwgImF0dHJpYnV0ZXMiOiB7Il91dWlkIjogeyJ0eXBlIjogIlVVSUQiLCAidXVpZCI6ICIyMDNjM2NlNi01Yzc5LTRkMGUtYjM2My04MmQ0ODQ4MGFiOTgifSwgImVsZW1lbnRzIjogeyJ0eXBlIjogImxpc3QiLCAiZWxlbWVudHMiOiBbeyJ0eXBlIjogIkZvckxvb3AiLCAiYXR0cmlidXRlcyI6IHsiX3V1aWQiOiB7InR5cGUiOiAiVVVJRCIsICJ1dWlkIjogImM4ZDY2MzM4LWM1NDktNDI3MC1iNDYwLTYwODZhNDkxNDgzMyJ9LCAiZWxlbWVudHMiOiB7InR5cGUiOiAibGlzdCIsICJlbGVtZW50cyI6IFt7InR5cGUiOiAiU2V0R2FpbiIsICJhdHRyaWJ1dGVzIjogeyJfdXVpZCI6IHsidHlwZSI6ICJVVUlEIiwgInV1aWQiOiAiZmRhZDIwMDgtYjg1Yi00YmI2LWIyMGItY2Y0NjZkMWRhZTU4In0sICJidXMiOiAiZHJpdmVfcTBfYnVzIiwgImdhaW4iOiB7InR5cGUiOiAiRmxvYXRWYXJpYWJsZSIsICJhdHRyaWJ1dGVzIjogeyJfdXVpZCI6IHsidHlwZSI6ICJVVUlEIiwgInV1aWQiOiAiNjM1ZGY3Y2EtY2UzOC00ZDYyLTlmZWQtN2YxY2JhZjcxZTc5In0sICJfc291cmNlIjogeyJ0eXBlIjogIlZhbHVlU291cmNlIiwgImF0dHJpYnV0ZXMiOiB7InZhbHVlIjogIkZyZWUifX0sICJfdmFsdWUiOiBudWxsLCAiX2RvbWFpbiI6IHsidHlwZSI6ICJEb21haW4iLCAiYXR0cmlidXRlcyI6IHsidmFsdWUiOiAiVm9sdGFnZSJ9fX19fX0sIHsidHlwZSI6ICJQbGF5IiwgImF0dHJpYnV0ZXMiOiB7Il91dWlkIjogeyJ0eXBlIjogIlVVSUQiLCAidXVpZCI6ICJhYmNhY2QxMS1lNGFhLTQyOWItYjYzYy0zYTI1MDliY2ExN2YifSwgImJ1cyI6ICJkcml2ZV9xMF9idXMiLCAid2F2ZWZvcm0iOiB7InR5cGUiOiAiSVFQYWlyIiwgImF0dHJpYnV0ZXMiOiB7IkkiOiB7InR5cGUiOiAiR2F1c3NpYW4iLCAiYXR0cmlidXRlcyI6IHsiYW1wbGl0dWRlIjogMS4wLCAiZHVyYXRpb24iOiA0MCwgIm51bV9zaWdtYXMiOiA0LjV9fSwgIlEiOiB7InR5cGUiOiAiRHJhZ0NvcnJlY3Rpb24iLCAiYXR0cmlidXRlcyI6IHsiZHJhZ19jb2VmZmljaWVudCI6IC0yLjAsICJ3YXZlZm9ybSI6IHsidHlwZSI6ICJHYXVzc2lhbiIsICJhdHRyaWJ1dGVzIjogeyJhbXBsaXR1ZGUiOiAxLjAsICJkdXJhdGlvbiI6IDQwLCAibnVtX3NpZ21hcyI6IDQuNX19fX19fSwgIndhaXRfdGltZSI6IG51bGx9fSwgeyJ0eXBlIjogIlN5bmMiLCAiYXR0cmlidXRlcyI6IHsiX3V1aWQiOiB7InR5cGUiOiAiVVVJRCIsICJ1dWlkIjogIjlkYWQyYWM2LWM5NTgtNGNkOS04NTMyLTJjMjMyYTUyZDM4NyJ9LCAiYnVzZXMiOiBudWxsfX0sIHsidHlwZSI6ICJQbGF5IiwgImF0dHJpYnV0ZXMiOiB7Il91dWlkIjogeyJ0eXBlIjogIlVVSUQiLCAidXVpZCI6ICI0ZTJhM2E3NS1iZGMxLTQxM2YtOGQ4NS02NzAzOTU4ZDM4NzUifSwgImJ1cyI6ICJyZWFkb3V0X3EwX2J1cyIsICJ3YXZlZm9ybSI6IHsidHlwZSI6ICJJUVBhaXIiLCAiYXR0cmlidXRlcyI6IHsiSSI6IHsidHlwZSI6ICJTcXVhcmUiLCAiYXR0cmlidXRlcyI6IHsiYW1wbGl0dWRlIjogMS4wLCAiZHVyYXRpb24iOiAyMDAwfX0sICJRIjogeyJ0eXBlIjogIlNxdWFyZSIsICJhdHRyaWJ1dGVzIjogeyJhbXBsaXR1ZGUiOiAwLjAsICJkdXJhdGlvbiI6IDIwMDB9fX19LCAid2FpdF90aW1lIjogNDB9fSwgeyJ0eXBlIjogIkFjcXVpcmUiLCAiYXR0cmlidXRlcyI6IHsiX3V1aWQiOiB7InR5cGUiOiAiVVVJRCIsICJ1dWlkIjogIjNmNmJjYWI3LTkyZTktNDNiOC04OWIwLTkzYjQ3MTAzYzQ5YSJ9LCAiYnVzIjogInJlYWRvdXRfcTBfYnVzIiwgIndlaWdodHMiOiB7InR5cGUiOiAiSVFQYWlyIiwgImF0dHJpYnV0ZXMiOiB7IkkiOiB7InR5cGUiOiAiU3F1YXJlIiwgImF0dHJpYnV0ZXMiOiB7ImFtcGxpdHVkZSI6IDEuMCwgImR1cmF0aW9uIjogMjAwMH19LCAiUSI6IHsidHlwZSI6ICJTcXVhcmUiLCAiYXR0cmlidXRlcyI6IHsiYW1wbGl0dWRlIjogMS4wLCAiZHVyYXRpb24iOiAyMDAwfX19fSwgIm5hbWUiOiBudWxsfX0sIHsidHlwZSI6ICJXYWl0IiwgImF0dHJpYnV0ZXMiOiB7Il91dWlkIjogeyJ0eXBlIjogIlVVSUQiLCAidXVpZCI6ICIzMzU0MzA3ZS1lNDk1LTQzYTMtYTgyNS0xOWRhM2U3MTEwNGUifSwgImJ1cyI6ICJyZWFkb3V0X3EwX2J1cyIsICJkdXJhdGlvbiI6IDEwMDAwfX1dfSwgInZhcmlhYmxlIjogeyJ0eXBlIjogIkZsb2F0VmFyaWFibGUiLCAiYXR0cmlidXRlcyI6IHsiX3V1aWQiOiB7InR5cGUiOiAiVVVJRCIsICJ1dWlkIjogIjYzNWRmN2NhLWNlMzgtNGQ2Mi05ZmVkLTdmMWNiYWY3MWU3OSJ9LCAiX3NvdXJjZSI6IHsidHlwZSI6ICJWYWx1ZVNvdXJjZSIsICJhdHRyaWJ1dGVzIjogeyJ2YWx1ZSI6ICJGcmVlIn19LCAiX3ZhbHVlIjogbnVsbCwgIl9kb21haW4iOiB7InR5cGUiOiAiRG9tYWluIiwgImF0dHJpYnV0ZXMiOiB7InZhbHVlIjogIlZvbHRhZ2UifX19fSwgInN0YXJ0IjogMC4wLCAic3RvcCI6IDEuMCwgInN0ZXAiOiAwLjF9fV19LCAic2hvdHMiOiAxMDAwfX1dfX19XX19fQ==",
        job_type="qprogram",
    )
    assert isinstance(job_result.data, dict)


def test_job_result_vqa_works():
    """Test vqa results are returned as dicts"""

    job_result = JobResult(
        job_id=0,
        http_response="eyJ2cWFfZGljdCI6IHsiX25hbWUiOiAiVlFBIiwgImFuc2F0eiI6IHsiX25hbWUiOiAiSGFyZHdhcmVFZmZpY2llbnRBbnNhdHoiLCAiX2NpcmN1aXQiOiB7Il90eXBlIjogIlF1YW50dW1DaXJjdWl0IiwgIl9nYXRlcyI6IFtdLCAiX2luaXRfc3RhdGUiOiBudWxsLCAibl9xdWJpdHMiOiA0fSwgIm5fcXViaXRzIjogNCwgImxheWVycyI6IDEsICJjb25uZWN0aXZpdHkiOiBbWzAsIDFdLCBbMSwgMl0sIFsyLCAzXV0sICJzdHJ1Y3R1cmUiOiAiZ3JvdXBlZCIsICJvbmVfZ2F0ZSI6ICJVMiIsICJ0d29fZ2F0ZSI6ICJDTk9UIn0sICJiYWNrZW5kIjogeyJfdHlwZSI6ICJRaWJvIiwgIl9jaXJjdWl0IjogbnVsbCwgImJhY2tlbmQiOiAibnVtcHkiLCAicGxhdGZvcm0iOiBudWxsfSwgImNvc3RfZnVuY3Rpb24iOiB7Il9uYW1lIjogIlRTUF9Db3N0RnVuY3Rpb24iLCAiaW5zdGFuY2UiOiB7Il9uYW1lIjogIlRTUF9JbnN0YW5jZSIsICJuX25vZGVzIjogMiwgInN0YXJ0IjogbnVsbCwgImxvb3AiOiB0cnVlLCAiX2Rpc3RhbmNlcyI6IFtbMC4wLCAwLjk2MzU3ODM4OTk0MjE5NzFdLCBbMC4zMTYzMTgyNzgxOTEzMjAzLCAwLjBdXX0sICJwYXJhbWV0ZXJzIjogW10sICJlbmNvZGluZyI6ICJvbmVfaG90IiwgImxhZ3JhbmdlX211bHRpcGxpZXIiOiAxMH0sICJpbnN0YW5jZSI6IHsiX25hbWUiOiAiVFNQX0luc3RhbmNlIiwgIm5fbm9kZXMiOiAyLCAic3RhcnQiOiBudWxsLCAibG9vcCI6IHRydWUsICJfZGlzdGFuY2VzIjogW1swLjAsIDAuOTYzNTc4Mzg5OTQyMTk3MV0sIFswLjMxNjMxODI3ODE5MTMyMDMsIDAuMF1dfSwgIm9wdGltaXplciI6IHsiX25hbWUiOiAiR3JhZGllbnREZXNjZW50In0sICJzYW1wbGVyIjogeyJfbmFtZSI6ICJTYW1wbGVyIiwgIl9jaXJjdWl0IjogbnVsbCwgIl9wYXJhbWV0ZXJzIjogW10sICJfcXVhbnR1bV9zdGF0ZSI6IG51bGwsICJfcHJvYmFiaWxpdHlfZGljdCI6IG51bGwsICJfcmVxdWlyZWRfcXViaXRzIjogbnVsbH0sICJuX3Nob3RzIjogMTAwMH0sICJpbml0X3BhcmFtcyI6IFswLCAwLCAwLCAwLCAwLCAwLCAwLCAwLCAwLCAwLCAwLCAwLCAwLCAwLCAwLCAwXSwgIm9wdGltaXplcl9wYXJhbXMiOiB7Im1ldGhvZCI6ICJQb3dlbGwifX0=",
        job_type="vqa",
    )
    assert isinstance(job_result.data, dict)


def test_job_result_program_raises_error():
    """Test we are rising exceptions to inform correctly that PROGRAMS are not currently supported."""

    job_result = JobResult(job_id=0, http_response="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==", job_type="program")
    assert isinstance(job_result.data, str)
