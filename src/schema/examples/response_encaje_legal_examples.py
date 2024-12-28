from src.schema.responses.response_encaje_legal_models import EncajeLegalGroupedResponseModel

# Ejemplo para respuesta 200 - Éxito
successful_response_example = {
    "description": "Successful Response - Grouped records from encaje_legal.",
    "content": {
        "application/json": {
            "example": {
                "fuente": "Banco Central",
                "reporte": "encaje_legal",
                "fecha_corte": {
                    "2024-12-20": [
                        {
                            "categoria": "Depósitos",
                            "subcategorias": [
                                {"subcategoria": "Ahorros", "valor": 125000.50}
                            ]
                        },
                        {
                            "categoria": "Préstamos",
                            "subcategorias": [
                                {"subcategoria": "Consumo", "valor": 85000.75}
                            ]
                        }
                    ],
                    "2024-12-19": [
                        {
                            "categoria": "Préstamos",
                            "subcategorias": [
                                {"subcategoria": "Hipotecarios", "valor": 150000.00}
                            ]
                        }
                    ]
                },
                "Total": {
                    "2024-12-20": [
                        {
                            "categoria": "Depósitos",
                            "subcategorias": [
                                {"subcategoria": "Ahorros", "valor_total": 125000.50}
                            ]
                        },
                        {
                            "categoria": "Préstamos",
                            "subcategorias": [
                                {"subcategoria": "Consumo", "valor_total": 85000.75}
                            ]
                        }
                    ],
                    "2024-12-19": [
                        {
                            "categoria": "Préstamos",
                            "subcategorias": [
                                {"subcategoria": "Hipotecarios", "valor_total": 150000.00}
                            ]
                        }
                    ]
                }
            }
        }
    }
}

# Ejemplo para respuesta 400 - Solicitud Incorrecta
bad_request_example = {
    "description": "Bad Request - Invalid or missing parameters.",
    "content": {
        "application/json": {
            "example": {
                "detail": "Invalid request. Required parameters are missing or incorrect."
            }
        }
    }
}

# Ejemplo para respuesta 404 - No Encontrado
not_found_example = {
    "description": "Not Found - Requested resource does not exist.",
    "content": {
        "application/json": {
            "example": {
                "detail": "No records found in encaje_legal for the specified query."
            }
        }
    }
}

# Ejemplo para respuesta 500 - Error Interno del Servidor
internal_server_error_example = {
    "description": "Internal Server Error - Unexpected error occurred.",
    "content": {
        "application/json": {
            "example": {
                "detail": "An unexpected error occurred. Please try again later."
            }
        }
    }
}

# Configuración de respuestas
encaje_legal_responses = {
    200: successful_response_example,
    400: bad_request_example,
    404: not_found_example,
    500: internal_server_error_example,
}
