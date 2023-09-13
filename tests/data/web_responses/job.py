"""Job listing web responses"""

import json

from requests import Response

from qiboconnection.typings.job import JobStatus, JobType

job_listing_item_response_a = {
    "user_id": 1,
    "device_id": 7,
    "status": JobStatus.COMPLETED,
    "job_type": JobType.CIRCUIT,
    "number_shots": 45,
    "id": None,
}
job_listing_item_response_b = {
    "user_id": 12,
    "device_id": 7,
    "status": JobStatus.PENDING,
    "job_type": JobType.EXPERIMENT,
    "number_shots": 45,
    "id": 45,
}

job_listing_item_response_c = {
    "title": "Bad Request",
    "status": 400,
    "detail": "Requested job with 'job_id': 8310, does not exist.",
}


class JobResponse:
    """mock job web responses"""

    @classmethod
    def retrieve_job_response_400_raw(cls):
        response = Response()
        response.status_code = 404
        response._content = json.dumps(
            {"title": "Bad Request", "detail": "Requested job with 'job_id': 8310, does not exist."}
        ).encode("utf-8")
        return response

    retrieve_job_listing_response: tuple[tuple[dict, int]] = (
        (
            {
                "items": [job_listing_item_response_a, job_listing_item_response_b],
                "total": 2,
                "per_page": 5,
                "self": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=1&per_page=5",
                "links": {
                    "first": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=1&per_page=5",
                    "prev": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=None&per_page=5",
                    "next": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=None&per_page=5",
                    "last": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=1&per_page=5",
                },
            },
            200,
        ),
    )

    delete_job_response: tuple[str, int] = ("", 204)
    delete_job_response_ise: tuple[str, int] = ("", 500)
    retrieve_job_response: tuple[dict[str, object], int] = (
        {
            "job_id": 10320,
            "user_id": 6,
            "device_id": 10,
            "status": "pending",
            "job_type": "experiment",
            "queue_position": 73,
            "description": "eyJwbGF0Zm9ybSI6IHsic2V0dGluZ3MiOiB7ImlkXyI6IDAsICJjYXRlZ29yeSI6ICJwbGF0Zm9ybSIsICJhbGlhcyI6IG51bGwsICJuYW1lIjogImdhbGFkcmllbCIsICJkZWxheV9iZXR3ZWVuX3B1bHNlcyI6IDAsICJkZWxheV9iZWZvcmVfcmVhZG91dCI6IDgwLjAsICJtYXN0ZXJfYW1wbGl0dWRlX2dhdGUiOiAxLCAibWFzdGVyX2R1cmF0aW9uX2dhdGUiOiAxMDAsICJnYXRlcyI6IFt7Im5hbWUiOiAiTSIsICJhbXBsaXR1ZGUiOiAibWFzdGVyX2FtcGxpdHVkZV9nYXRlIiwgInBoYXNlIjogMCwgImR1cmF0aW9uIjogMjAwMCwgInNoYXBlIjogeyJuYW1lIjogInJlY3Rhbmd1bGFyIn19LCB7Im5hbWUiOiAiSSIsICJhbXBsaXR1ZGUiOiAwLCAicGhhc2UiOiAwLCAiZHVyYXRpb24iOiAwLCAic2hhcGUiOiB7Im5hbWUiOiAicmVjdGFuZ3VsYXIifX0sIHsibmFtZSI6ICJYIiwgImFtcGxpdHVkZSI6ICJtYXN0ZXJfYW1wbGl0dWRlX2dhdGUiLCAicGhhc2UiOiAwLCAiZHVyYXRpb24iOiAibWFzdGVyX2R1cmF0aW9uX2dhdGUiLCAic2hhcGUiOiB7Im5hbWUiOiAiZHJhZyIsICJudW1fc2lnbWFzIjogNCwgImRyYWdfY29lZmZpY2llbnQiOiAwfX0sIHsibmFtZSI6ICJZIiwgImFtcGxpdHVkZSI6ICJtYXN0ZXJfYW1wbGl0dWRlX2dhdGUiLCAicGhhc2UiOiAxLjU3MDc5NjMyNjc5NDg5NjYsICJkdXJhdGlvbiI6ICJtYXN0ZXJfZHVyYXRpb25fZ2F0ZSIsICJzaGFwZSI6IHsibmFtZSI6ICJkcmFnIiwgIm51bV9zaWdtYXMiOiA0LCAiZHJhZ19jb2VmZmljaWVudCI6IDB9fV19LCAic2NoZW1hIjogeyJjaGlwIjogeyJpZF8iOiAwLCAiY2F0ZWdvcnkiOiAiY2hpcCIsICJub2RlcyI6IFt7Im5hbWUiOiAicG9ydCIsICJpZF8iOiAwLCAiY2F0ZWdvcnkiOiAibm9kZSIsICJhbGlhcyI6IG51bGwsICJub2RlcyI6IFszXX0sIHsibmFtZSI6ICJwb3J0IiwgImlkXyI6IDEsICJjYXRlZ29yeSI6ICJub2RlIiwgImFsaWFzIjogbnVsbCwgIm5vZGVzIjogWzJdfSwgeyJuYW1lIjogInJlc29uYXRvciIsICJpZF8iOiAyLCAiY2F0ZWdvcnkiOiAibm9kZSIsICJhbGlhcyI6ICJyZXNvbmF0b3IiLCAibm9kZXMiOiBbMSwgM10sICJmcmVxdWVuY3kiOiA3MzQ3MzAwMDAwLjB9LCB7Im5hbWUiOiAicXViaXQiLCAiaWRfIjogMywgImNhdGVnb3J5IjogIm5vZGUiLCAiYWxpYXMiOiAicXViaXQiLCAibm9kZXMiOiBbMCwgMl0sICJmcmVxdWVuY3kiOiAzNDUxMDAwMDAwLjAsICJxdWJpdF9pZHgiOiAwfV19LCAiaW5zdHJ1bWVudHMiOiBbeyJuYW1lIjogIlFDTSIsICJpZF8iOiAwLCAiY2F0ZWdvcnkiOiAiYXdnIiwgImFsaWFzIjogIlFDTSIsICJmaXJtd2FyZSI6ICIwLjcuMCIsICJmcmVxdWVuY3kiOiAxLjAsICJudW1fc2VxdWVuY2VycyI6IDEsICJnYWluIjogWzFdLCAiZXBzaWxvbiI6IFswXSwgImRlbHRhIjogWzBdLCAib2Zmc2V0X2kiOiBbMF0sICJvZmZzZXRfcSI6IFswXSwgIm11bHRpcGxleGluZ19mcmVxdWVuY2llcyI6IFsxMDAwMDAwMDAuMF0sICJzeW5jX2VuYWJsZWQiOiB0cnVlLCAibnVtX2JpbnMiOiAxMDB9LCB7Im5hbWUiOiAiUVJNIiwgImlkXyI6IDEsICJjYXRlZ29yeSI6ICJhd2ciLCAiYWxpYXMiOiAiUVJNIiwgImZpcm13YXJlIjogIjAuNy4wIiwgImZyZXF1ZW5jeSI6IDIwMDAwMDAwLCAibnVtX3NlcXVlbmNlcnMiOiAxLCAiZ2FpbiI6IFswLjVdLCAiZXBzaWxvbiI6IFswXSwgImRlbHRhIjogWzBdLCAib2Zmc2V0X2kiOiBbMF0sICJvZmZzZXRfcSI6IFswXSwgIm11bHRpcGxleGluZ19mcmVxdWVuY2llcyI6IFsyMDAwMDAwMC4wXSwgImFjcXVpc2l0aW9uX2RlbGF5X3RpbWUiOiAxMDAsICJzeW5jX2VuYWJsZWQiOiB0cnVlLCAibnVtX2JpbnMiOiAxMDAsICJzY29wZV9hY3F1aXJlX3RyaWdnZXJfbW9kZSI6ICJzZXF1ZW5jZXIiLCAic2NvcGVfaGFyZHdhcmVfYXZlcmFnaW5nIjogdHJ1ZSwgInNhbXBsaW5nX3JhdGUiOiAxMDAwMDAwMDAwLCAiaW50ZWdyYXRpb24iOiB0cnVlLCAiaW50ZWdyYXRpb25fbGVuZ3RoIjogMjAwMCwgImludGVncmF0aW9uX21vZGUiOiAic3NiIiwgInNlcXVlbmNlX3RpbWVvdXQiOiAxLCAiYWNxdWlzaXRpb25fdGltZW91dCI6IDF9LCB7Im5hbWUiOiAicm9oZGVfc2Nod2FyeiIsICJpZF8iOiAwLCAiY2F0ZWdvcnkiOiAic2lnbmFsX2dlbmVyYXRvciIsICJhbGlhcyI6ICJyc18wIiwgImZpcm13YXJlIjogIjQuMzAuMDQ2LjI5NSIsICJwb3dlciI6IDE1fSwgeyJuYW1lIjogInJvaGRlX3NjaHdhcnoiLCAiaWRfIjogMSwgImNhdGVnb3J5IjogInNpZ25hbF9nZW5lcmF0b3IiLCAiYWxpYXMiOiAicnNfMSIsICJmaXJtd2FyZSI6ICI0LjMwLjA0Ni4yOTUiLCAicG93ZXIiOiAxNX0sIHsibmFtZSI6ICJtaW5pX2NpcmN1aXRzIiwgImlkXyI6IDEsICJjYXRlZ29yeSI6ICJhdHRlbnVhdG9yIiwgImFsaWFzIjogImF0dGVudWF0b3IiLCAiZmlybXdhcmUiOiBudWxsLCAiYXR0ZW51YXRpb24iOiAzMH0sIHsibmFtZSI6ICJrZWl0aGxleV8yNjAwIiwgImlkXyI6IDEsICJjYXRlZ29yeSI6ICJkY19zb3VyY2UiLCAiYWxpYXMiOiAia2VpdGhsZXlfMjYwMCIsICJmaXJtd2FyZSI6IG51bGwsICJtYXhfY3VycmVudCI6IDAuMSwgIm1heF92b2x0YWdlIjogMjAuMH1dLCAiYnVzZXMiOiBbeyJpZF8iOiAwLCAiY2F0ZWdvcnkiOiAiYnVzIiwgInN1YmNhdGVnb3J5IjogImNvbnRyb2wiLCAic3lzdGVtX2NvbnRyb2wiOiB7ImlkXyI6IDAsICJjYXRlZ29yeSI6ICJzeXN0ZW1fY29udHJvbCIsICJzdWJjYXRlZ29yeSI6ICJtaXhlcl9iYXNlZF9zeXN0ZW1fY29udHJvbCIsICJhd2ciOiAiUUNNIiwgInNpZ25hbF9nZW5lcmF0b3IiOiAicnNfMCJ9LCAicG9ydCI6IDB9LCB7ImlkXyI6IDAsICJjYXRlZ29yeSI6ICJidXMiLCAic3ViY2F0ZWdvcnkiOiAicmVhZG91dCIsICJzeXN0ZW1fY29udHJvbCI6IHsiaWRfIjogMSwgImNhdGVnb3J5IjogInN5c3RlbV9jb250cm9sIiwgInN1YmNhdGVnb3J5IjogIm1peGVyX2Jhc2VkX3N5c3RlbV9jb250cm9sIiwgImF3ZyI6ICJRUk0iLCAic2lnbmFsX2dlbmVyYXRvciI6ICJyc18xIn0sICJhdHRlbnVhdG9yIjogImF0dGVudWF0b3IiLCAicG9ydCI6IDF9XSwgImluc3RydW1lbnRfY29udHJvbGxlcnMiOiBbeyJuYW1lIjogInFibG94X3B1bHNhciIsICJpZF8iOiAwLCAiYWxpYXMiOiAicHVsc2FyX2NvbnRyb2xsZXJfcWNtXzAiLCAiY2F0ZWdvcnkiOiAiaW5zdHJ1bWVudF9jb250cm9sbGVyIiwgInN1YmNhdGVnb3J5IjogInNpbmdsZV9pbnN0cnVtZW50IiwgImNvbm5lY3Rpb24iOiB7Im5hbWUiOiAidGNwX2lwIiwgImFkZHJlc3MiOiAiMTkyLjE2OC4wLjMifSwgIm1vZHVsZXMiOiBbeyJhd2ciOiAiUUNNIiwgInNsb3RfaWQiOiAwfV0sICJyZWZlcmVuY2VfY2xvY2siOiAiaW50ZXJuYWwifSwgeyJuYW1lIjogInFibG94X3B1bHNhciIsICJpZF8iOiAxLCAiYWxpYXMiOiAicHVsc2FyX2NvbnRyb2xsZXJfcXJtXzAiLCAiY2F0ZWdvcnkiOiAiaW5zdHJ1bWVudF9jb250cm9sbGVyIiwgInN1YmNhdGVnb3J5IjogInNpbmdsZV9pbnN0cnVtZW50IiwgImNvbm5lY3Rpb24iOiB7Im5hbWUiOiAidGNwX2lwIiwgImFkZHJlc3MiOiAiMTkyLjE2OC4wLjQifSwgIm1vZHVsZXMiOiBbeyJhd2ciOiAiUVJNIiwgInNsb3RfaWQiOiAwfV0sICJyZWZlcmVuY2VfY2xvY2siOiAiZXh0ZXJuYWwifSwgeyJuYW1lIjogInJvaGRlX3NjaHdhcnoiLCAiaWRfIjogMiwgImFsaWFzIjogInJvaGRlX3NjaHdhcnpfY29udHJvbGxlcl8wIiwgImNhdGVnb3J5IjogImluc3RydW1lbnRfY29udHJvbGxlciIsICJzdWJjYXRlZ29yeSI6ICJzaW5nbGVfaW5zdHJ1bWVudCIsICJjb25uZWN0aW9uIjogeyJuYW1lIjogInRjcF9pcCIsICJhZGRyZXNzIjogIjE5Mi4xNjguMC4xMCJ9LCAibW9kdWxlcyI6IFt7InNpZ25hbF9nZW5lcmF0b3IiOiAicnNfMCIsICJzbG90X2lkIjogMH1dfSwgeyJuYW1lIjogInJvaGRlX3NjaHdhcnoiLCAiaWRfIjogMywgImFsaWFzIjogInJvaGRlX3NjaHdhcnpfY29udHJvbGxlcl8xIiwgImNhdGVnb3J5IjogImluc3RydW1lbnRfY29udHJvbGxlciIsICJzdWJjYXRlZ29yeSI6ICJzaW5nbGVfaW5zdHJ1bWVudCIsICJjb25uZWN0aW9uIjogeyJuYW1lIjogInRjcF9pcCIsICJhZGRyZXNzIjogIjE5Mi4xNjguMC43In0sICJtb2R1bGVzIjogW3sic2lnbmFsX2dlbmVyYXRvciI6ICJyc18xIiwgInNsb3RfaWQiOiAwfV19LCB7Im5hbWUiOiAibWluaV9jaXJjdWl0cyIsICJpZF8iOiA0LCAiYWxpYXMiOiAiYXR0ZW51YXRvcl9jb250cm9sbGVyXzAiLCAiY2F0ZWdvcnkiOiAiaW5zdHJ1bWVudF9jb250cm9sbGVyIiwgInN1YmNhdGVnb3J5IjogInNpbmdsZV9pbnN0cnVtZW50IiwgImNvbm5lY3Rpb24iOiB7Im5hbWUiOiAidGNwX2lwIiwgImFkZHJlc3MiOiAiMTkyLjE2OC4wLjIyMiJ9LCAibW9kdWxlcyI6IFt7ImF0dGVudWF0b3IiOiAiYXR0ZW51YXRvciIsICJzbG90X2lkIjogMH1dfSwgeyJuYW1lIjogImtlaXRobGV5XzI2MDAiLCAiaWRfIjogNSwgImFsaWFzIjogImtlaXRobGV5XzI2MDBfY29udHJvbGxlcl8wIiwgImNhdGVnb3J5IjogImluc3RydW1lbnRfY29udHJvbGxlciIsICJzdWJjYXRlZ29yeSI6ICJzaW5nbGVfaW5zdHJ1bWVudCIsICJjb25uZWN0aW9uIjogeyJuYW1lIjogInRjcF9pcCIsICJhZGRyZXNzIjogIjE5Mi4xNjguMC4xMTIifSwgIm1vZHVsZXMiOiBbeyJkY19zb3VyY2UiOiAia2VpdGhsZXlfMjYwMCIsICJzbG90X2lkIjogMH1dfV19fSwgInNldHRpbmdzIjogeyJoYXJkd2FyZV9hdmVyYWdlIjogMTAyNCwgInNvZnR3YXJlX2F2ZXJhZ2UiOiAxLCAicmVwZXRpdGlvbl9kdXJhdGlvbiI6IDIwMDAwMH0sICJzZXF1ZW5jZXMiOiBbeyJlbGVtZW50cyI6IFt7InRpbWVsaW5lIjogW3sicHVsc2UiOiB7Im5hbWUiOiAicHVsc2UiLCAiYW1wbGl0dWRlIjogMS4wLCAiZnJlcXVlbmN5IjogbnVsbCwgInBoYXNlIjogMC4wLCAiZHVyYXRpb24iOiAxMDAsICJwdWxzZV9zaGFwZSI6IHsibmFtZSI6ICJkcmFnIiwgIm51bV9zaWdtYXMiOiA0LCAiZHJhZ19jb2VmZmljaWVudCI6IDB9fSwgInN0YXJ0X3RpbWUiOiAwfSwgeyJwdWxzZSI6IHsibmFtZSI6ICJwdWxzZSIsICJhbXBsaXR1ZGUiOiAxLjAsICJmcmVxdWVuY3kiOiBudWxsLCAicGhhc2UiOiAxLjU3MDc5NjMyNjc5NDg5NjYsICJkdXJhdGlvbiI6IDEwMCwgInB1bHNlX3NoYXBlIjogeyJuYW1lIjogImRyYWciLCAibnVtX3NpZ21hcyI6IDQsICJkcmFnX2NvZWZmaWNpZW50IjogMH19LCAic3RhcnRfdGltZSI6IDEwMH0sIHsicHVsc2UiOiB7Im5hbWUiOiAicHVsc2UiLCAiYW1wbGl0dWRlIjogMC42Nzg4NzI2MTc3NzI4MTQzLCAiZnJlcXVlbmN5IjogbnVsbCwgInBoYXNlIjogMy4xNDE1OTI2NTM1ODk3OTMsICJkdXJhdGlvbiI6IDEwMCwgInB1bHNlX3NoYXBlIjogeyJuYW1lIjogImRyYWciLCAibnVtX3NpZ21hcyI6IDQsICJkcmFnX2NvZWZmaWNpZW50IjogMH19LCAic3RhcnRfdGltZSI6IDIwMH0sIHsicHVsc2UiOiB7Im5hbWUiOiAicHVsc2UiLCAiYW1wbGl0dWRlIjogMC43NzQ2NDgyOTI3NTY4NjAzLCAiZnJlcXVlbmN5IjogbnVsbCwgInBoYXNlIjogMS41NzA3OTYzMjY3OTQ4OTY2LCAiZHVyYXRpb24iOiAxMDAsICJwdWxzZV9zaGFwZSI6IHsibmFtZSI6ICJkcmFnIiwgIm51bV9zaWdtYXMiOiA0LCAiZHJhZ19jb2VmZmljaWVudCI6IDB9fSwgInN0YXJ0X3RpbWUiOiAzMDB9LCB7InB1bHNlIjogeyJuYW1lIjogInB1bHNlIiwgImFtcGxpdHVkZSI6IDAuNDU2MzM4NDA2NTczMDY5NTcsICJmcmVxdWVuY3kiOiBudWxsLCAicGhhc2UiOiA2LjE1MDQ0NDA3ODQ2MTI0MSwgImR1cmF0aW9uIjogMTAwLCAicHVsc2Vfc2hhcGUiOiB7Im5hbWUiOiAiZHJhZyIsICJudW1fc2lnbWFzIjogNCwgImRyYWdfY29lZmZpY2llbnQiOiAwfX0sICJzdGFydF90aW1lIjogNDAwfV0sICJwb3J0IjogMH0sIHsidGltZWxpbmUiOiBbeyJwdWxzZSI6IHsibmFtZSI6ICJyZWFkb3V0X3B1bHNlIiwgImFtcGxpdHVkZSI6IDEsICJmcmVxdWVuY3kiOiBudWxsLCAicGhhc2UiOiAwLCAiZHVyYXRpb24iOiAyMDAwLCAicHVsc2Vfc2hhcGUiOiB7Im5hbWUiOiAicmVjdGFuZ3VsYXIifX0sICJzdGFydF90aW1lIjogNTgwLjB9XSwgInBvcnQiOiAxfV19XSwgImxvb3BzIjogW3siYWxpYXMiOiBudWxsLCAiaW5zdHJ1bWVudCI6ICJzaWduYWxfZ2VuZXJhdG9yIiwgImlkXyI6IDAsICJwYXJhbWV0ZXIiOiAiZnJlcXVlbmN5IiwgInN0YXJ0IjogMCwgInN0b3AiOiAxLCAibnVtIjogMiwgInN0ZXAiOiBudWxsLCAibG9vcCI6IHsiYWxpYXMiOiAicGxhdGZvcm0iLCAiaW5zdHJ1bWVudCI6IG51bGwsICJpZF8iOiBudWxsLCAicGFyYW1ldGVyIjogImRlbGF5X2JlZm9yZV9yZWFkb3V0IiwgInN0YXJ0IjogNDAsICJzdG9wIjogMTAwLCAibnVtIjogbnVsbCwgInN0ZXAiOiA0MCwgImxvb3AiOiB7ImFsaWFzIjogbnVsbCwgImluc3RydW1lbnQiOiAiYXdnIiwgImlkXyI6IDAsICJwYXJhbWV0ZXIiOiAiZnJlcXVlbmN5IiwgInN0YXJ0IjogMCwgInN0b3AiOiAxLCAibnVtIjogMiwgInN0ZXAiOiBudWxsLCAibG9vcCI6IG51bGx9fX1dLCAibmFtZSI6ICJleHBlcmltZW50In0=",
            "number_shots": 10,
            "result": None,
        },
        200,
    )