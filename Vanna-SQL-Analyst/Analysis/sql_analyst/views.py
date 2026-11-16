from django.shortcuts import render

# Create your views here.

import json
import re
import sqlite3
from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .Engine import get_vanna


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "database" / "retail.db"


@csrf_exempt
@require_POST
def sql_analyst_api(request):
    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()

        if not question:
            return JsonResponse(
                {"error": "Question is required."},
                status=400
            )

        vn = get_vanna()
        sql = vn.generate_sql(question=question)

        if not sql or not re.match(r"^\s*(SELECT|WITH)\b", sql, re.IGNORECASE):
            return JsonResponse(
                {"error": "Generated SQL is not an accepted read query."},
                status=400
            )

        # Execute against the database in read-only mode
        database_uri = DATABASE_PATH.resolve().as_uri() + "?mode=ro"

        with sqlite3.connect(database_uri, uri=True) as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

        results = [
            dict(zip(columns, row))
            for row in rows
        ]

        return JsonResponse({
            "question": question,
            "sql": sql,
            "results": results
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON request."}, status=400)

    except Exception as error:
        return JsonResponse({"error": str(error)}, status=500)
