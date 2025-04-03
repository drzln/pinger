import json
from lcs.athena import athena
from lcs.config import config


def athena_lambda_handler(event, _):
    action = event.get("action")

    if action == "start_query":
        query = event.get("query")
        database = event.get("database")
        output_location = event.get("outputLocation")

        if not query or not database or not output_location:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": "Missing required parameters for start_query"}
                ),
                "isBase64Encoded": False,
                "headers": {"content-type": "application/json"},
            }

        query_id = athena().start_query(query, database, output_location)

        # Echo back all relevant input + the new query ID
        response_payload = {
            "status": "SUCCEEDED",
            "statusCode": 200,
            "queryExecutionId": query_id,
            "query": query,
            "database": database,
            "outputLocation": output_location,
            "wait_seconds": event.get("wait_seconds"),
            "reportName": event.get("reportName"),
            "requestId": event.get("requestId"),
        }

        return response_payload

    elif action == "wait_for_query":
        query_id = event.get("queryExecutionId")
        timeout = int(event.get("timeout", 300))
        interval = int(event.get("interval", 5))

        if not query_id:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": "Missing queryExecutionId for wait_for_query"}
                ),
                "isBase64Encoded": False,
                "headers": {"content-type": "application/json"},
            }

        try:
            result = athena().wait_for_query(
                query_id, timeout=timeout, interval=interval
            )
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)}),
                "isBase64Encoded": False,
                "headers": {"content-type": "application/json"},
            }

        if "QueryExecution" in result and "Status" in result["QueryExecution"]:
            result["QueryExecution"]["Status"].pop("SubmissionDateTime", None)
            result["QueryExecution"]["Status"].pop("CompletionDateTime", None)
        result["statusCode"] = 200
        result["status"] = "SUCCEEDED"
        result["isBase64Encoded"] = False
        result["headers"] = {"content-type": "application/json"}
        return result

    elif action == "query_metadata":
        query_id = event.get("queryExecutionId")
        if not query_id:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": "Missing queryExecutionId for query_metadata"}
                ),
                "isBase64Encoded": False,
                "headers": {"content-type": "application/json"},
            }
        metadata = athena().query_metadata(query_id)
        return {
            "statusCode": 200,
            "body": json.dumps(metadata),
            "isBase64Encoded": False,
            "headers": {"content-type": "application/json"},
        }

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid action"}),
            "isBase64Encoded": False,
            "headers": {"content-type": "application/json"},
        }
