import os
import json
import csv
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd

class DataSaver:
    """Class for saving generated data in different formats."""
    
    def save_data(self, data: List[Dict[str, Any]], output_format: str, output_dir: str) -> str:
        """Save the generated data to a file.
        
        Args:
            data: The data to save
            output_format: Format to save the data in (json, csv, parquet)
            output_dir: Directory to save the file in
            
        Returns:
            Path to the saved file
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"synthetic_data_{timestamp}.{output_format}"
            filepath = os.path.join(output_dir, filename)
            
            # Save the data
            if output_format == "json":
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)
            elif output_format == "csv":
                with open(filepath, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            elif output_format == "parquet":
                df = pd.DataFrame(data)
                df.to_parquet(filepath)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            print(f"\nData saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"\nError saving data: {str(e)}")
            raise 