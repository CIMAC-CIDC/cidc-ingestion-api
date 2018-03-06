#!/usr/bin/env python
"""
Settings file that lays out the database schema, as well as other constant variables.
"""

MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_USERNAME = 'python-eve'
MONGO_PASSWORD = 'apple'
MONGO_DBNAME = 'CIDC'
GOOGLE_URL = "gs://lloyd-test-pipeline/"
GOOGLE_FOLDER_PATH = "Experimental-Data/"
RABBITMQ_URI = "rabbitmq:5762"

# If this line is missing API will default to GET only
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT), and delete
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

ACCOUNTS = {
    'resource_methods': ['GET'],
    # Disable endpoint caching so clients don't cache account data
    'cache_control': '',
    'cache_expires': 0,
    'allowed_roles': ['superuser', 'admin'],
    'schema': {
        'token': {
            'type': 'string',
            'required': True,
        }
    },
}

DATA = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['admin', 'user'],
    'schema': {
        'file_name': {
            'type': 'string',
            'required': True,
        },
        'sample_id': {
            'type': 'string',
            'required': True,
        },
        'trial': {
            'type': 'objectid',
            'required': True,
        },
        'gs_uri': {
            'type': 'string',
            'required': True,
        },
        'assay': {
            'type': 'objectid',
            'required': True,
        },
        'date_created': {
            'type': 'string',
            'required': True,
        },
        'analysis_id': {
            'type': 'objectid',
        },
    }
}

# Aggregation query that groups data by Sample ID
DATA_AGG = {
    'datasource': {
        'source': 'data',
        'aggregation': {
            'pipeline': [
                {'$match': {'trial': '$trial', 'assay': '$assay'}},
                {
                    '$group': {
                        '_id': '$sample_id',
                        'records': {
                            '$push': {
                                'file_name': '$file_name',
                                'gs_uri': '$gs_uri'
                            }
                        }
                    }
                }
            ]
        }
    }
}

ANALYSIS = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['admin', 'superuser', 'user'],
    'schema': {
        'started_by': {
            'type': 'string',
            'required': True
        },
        'trial': {
            'type': 'objectid',
            'required': True
        },
        'assay': {
            'type': 'objectid',
            'required': True
        },
        'status': {
            'type': 'dict',
            'schema': {
                'progress': {
                    'type': 'string',
                    'allowed': ['In Progress', 'Completed', 'Aborted']
                },
                'message': {
                    'type': 'string'
                }
            }
        },
        'samples': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        },
        'metadata_blob': {
            'type': 'string'
        },
        'files_generated': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'file_name': {
                        'type': 'string',
                        'required': True
                    },
                    'gs_uri': {
                        'type': 'string',
                        'required': True
                    }
                }
            }
        }
    }
}

ASSAYS = {
    'public_methods': [],
    'resource_methods': ['GET'],
    'allowed_roles': ['admin', 'superuser', 'user'],
    'schema': {
        '_id': {
            'type': 'objectid',
            'required': True,
            'unique': True
        },
        'wdl_location': {
            'type': 'string'
        },
        'assay_name': {
            'type': 'string',
            'required': True
        },
        'static_inputs': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'key_name': {
                        'type': 'string',
                    },
                    'key_value': {
                        'type': 'unknown',
                    },
                },
            },
        },
        'workflow': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'step_name': {
                        'type': 'string',
                    },
                    'inputs': {
                        'type': 'list',
                        'schema': {
                            'type': 'string'
                        },
                    },
                    'outputs': {
                        'type': 'list',
                        'schema': {
                            'type': 'string'
                        },
                    },
                },
            },
        },
    },
}

TRIALS = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['user', 'admin', 'superuser'],
    'schema': {
        'trial_name': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'principal_investigator': {
            'type': 'string',
            'required': True,
        },
        'collaborators': {
            'type': 'list',
            'schema': {
                'type': 'string'
            },
        },
        'start_date': {
            'type': 'string',
            'required': True,
        },
        'assays': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'assay_name': {
                        'type': 'string',
                        'required': True
                    },
                    'assay_id': {
                        'type': 'string',
                        'required': True
                    }
                }
            },
        },
        'samples': {
            'type': 'list',
            'schema': {
                'type': 'string',
            }
        },
    },
}

# Schema that keeps track of jobs that users have started, as well as their ultimate status and
# fate
INGESTION = {
    'public_methods': [],
    'resource_methods': ['GET', 'POST'],
    'allowed_roles': ['user', 'superuser', 'admin'],
    'schema': {
        'number_of_files': {
            'type': 'integer',
            'required': True,
        },
        'started_by': {
            'type': 'string',
            'required': True,
        },
        'status': {
            'type': 'dict',
            'schema': {
                'progress': {
                    'type': 'string',
                    'allowed': ['In Progress', 'Completed', 'Aborted']
                },
                'message': {
                    'type': 'string'
                },
            }
        },
        'start_time': {
            'type': 'string'
        },
        'end_time': {
            'type': 'string',
        },
        'files': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'assay': {
                        'type': 'objectid',
                        'required': True
                    },
                    'trial': {
                        'type': 'objectid',
                        'required': True
                    },
                    'file_name': {
                        'type': 'string',
                        'required': True
                    },
                    'sample_id': {
                        'type': 'string',
                        'required': True
                    },
                },
            },
        },
    },
}

TEST = {
    'schema': {
        'message': {
            'type': 'string',
            'required': False
        }
    },
    'authentication': None
}

DOMAIN = {
    'accounts': ACCOUNTS,
    'ingestion': INGESTION,
    'data': DATA,
    'trials': TRIALS,
    'test': TEST,
    'assays': ASSAYS,
    'analysis': ANALYSIS,
    'data/query': DATA_AGG
}
