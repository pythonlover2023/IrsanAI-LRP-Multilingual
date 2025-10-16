{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "IrsanAI Report Schema",
  "description": "JSON-Schema für IrsanAI-Report-Dateien",
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["success", "challenges", "error"],
      "description": "Gesamtstatus des Reports"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Zeitpunkt der Report-Erstellung"
    },
    "report_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+$",
      "description": "Version des Report-Formats"
    },
    "unique_key": {
      "type": "string",
      "description": "Einzigartiger Schlüssel für Workflow-Tracking"
    },
    "task_id": {
      "type": "string",
      "description": "ID des ursprünglichen Tasks"
    },
    "os_info": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "version": {"type": "string"},
        "details": {
          "type": "object",
          "properties": {
            "full_version": {"type": "string"},
            "architecture": {"type": "string"},
            "processor": {"type": "string"}
          },
          "required": ["full_version", "architecture", "processor"]
        }
      },
      "required": ["name", "version", "details"]
    },
    "cpu_info": {
      "type": "object",
      "properties": {
        "physical_cores": {"type": "integer"},
        "logical_cores": {"type": "integer"},
        "max_frequency_mhz": {"type": ["integer", "null"]},
        "model": {"type": "string"}
      },
      "required": ["physical_cores", "logical_cores", "model"]
    },
    "memory_info": {
      "type": "object",
      "properties": {
        "total_mb": {"type": "integer"},
        "available_mb": {"type": "integer"}
      },
      "required": ["total_mb", "available_mb"]
    },
    "gpu_info": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "driver_version": {"type": "string"},
          "memory_total": {"type": "integer"},
          "anonymized_id": {"type": "string"}
        },
        "required": ["name", "driver_version", "memory_total", "anonymized_id"]
      }
    },
    "screen_info": {
      "type": "object",
      "properties": {
        "width": {"type": "integer"},
        "height": {"type": "integer"},
        "dpi": {"type": "integer"}
      },
      "required": ["width", "height", "dpi"]
    },
    "error_details": {
      "type": ["object", "null"],
      "description": "Fehlerdetails bei status=error oder status=challenges",
      "properties": {
        "error_type": {"type": "string"},
        "error_message": {"type": "string"},
        "code_line": {"type": ["integer", "null"]},
        "stack_trace": {"type": ["string", "null"]}
      }
    },
    "environment": {
      "type": "object",
      "description": "Informationen zur Ausführungsumgebung",
      "properties": {
        "ide": {"type": "string"},
        "os": {"type": "string"},
        "python_version": {"type": "string"}
      },
      "required": ["ide", "os", "python_version"]
    }
  },
  "required": [
    "status", "timestamp", "report_version", "unique_key", "task_id",
    "os_info", "cpu_info", "memory_info", "gpu_info", "screen_info"
  ]
}