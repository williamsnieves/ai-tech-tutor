from typing import Dict, Any

class PromptGenerator:
    """Class for generating prompts for different data types."""
    
    def __init__(self):
        """Initialize the prompt generator."""
        self._schemas = {
            "health": """{
                "patient_id": "string",
                "age": "integer",
                "gender": "string",
                "diagnosis": "string",
                "treatment": "string",
                "admission_date": "string",
                "discharge_date": "string"
            }""",
            "business": """{
                "company_id": "string",
                "name": "string",
                "industry": "string",
                "revenue": "float",
                "employees": "integer",
                "location": "string",
                "founded_year": "integer"
            }""",
            "e-commerce": """{
                "order_id": "string",
                "customer_id": "string",
                "product": "string",
                "quantity": "integer",
                "price": "float",
                "order_date": "string",
                "shipping_address": "string"
            }"""
        }
        
        self._examples = {
            "health": """[
    {
        "patient_id": "PAT001",
        "age": 45,
        "gender": "Female",
        "diagnosis": "Hypertension",
        "treatment": "Lisinopril 10mg daily",
        "admission_date": "2023-05-15",
        "discharge_date": "2023-05-17"
    },
    {
        "patient_id": "PAT002",
        "age": 32,
        "gender": "Male",
        "diagnosis": "Type 2 Diabetes",
        "treatment": "Metformin 500mg twice daily",
        "admission_date": "2023-06-01",
        "discharge_date": "2023-06-03"
    }
]""",
            "business": """[
    {
        "company_id": "COMP001",
        "name": "TechCorp Solutions",
        "industry": "Technology",
        "revenue": 1500000.00,
        "employees": 50,
        "location": "San Francisco, CA",
        "founded_year": 2015
    },
    {
        "company_id": "COMP002",
        "name": "GreenEnergy Systems",
        "industry": "Renewable Energy",
        "revenue": 2500000.00,
        "employees": 75,
        "location": "Austin, TX",
        "founded_year": 2018
    }
]""",
            "e-commerce": """[
    {
        "order_id": "ORD001",
        "customer_id": "CUST001",
        "product": "Wireless Headphones",
        "quantity": 1,
        "price": 99.99,
        "order_date": "2023-07-15",
        "shipping_address": "123 Main St, New York, NY 10001"
    },
    {
        "order_id": "ORD002",
        "customer_id": "CUST002",
        "product": "Smart Watch",
        "quantity": 2,
        "price": 199.99,
        "order_date": "2023-07-16",
        "shipping_address": "456 Oak Ave, Los Angeles, CA 90001"
    }
]"""
        }
    
    def create_prompt(self, data_type: str, sample_size: int) -> str:
        """Create a prompt for data generation.
        
        Args:
            data_type: Type of data to generate
            sample_size: Number of samples to generate
            
        Returns:
            Formatted prompt string
        """
        if data_type not in self._schemas:
            raise ValueError(f"Unsupported data type: {data_type}")
            
        schema = self._schemas[data_type]
        example = self._examples[data_type]
        
        return f"""Generate {sample_size} realistic {data_type} records in JSON format.
The data should follow this schema:
{schema}

Here's an example of the expected format:
{example}

Generate {sample_size} unique records following the same format and schema.
Make sure the data is realistic and varied.
Return only the JSON array, without any additional text or explanation.""" 