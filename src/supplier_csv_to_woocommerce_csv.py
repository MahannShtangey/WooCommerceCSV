"""
File:           supplier_csv_to_woocommerce_csv.py
Author:         Dibyaranjan Sathua
Created on:     25/12/2020, 11:56
"""
from typing import Optional, List, Dict
import pandas as pd
import yaml
from src.template import Template


class SupplierCSV2WoocommerceCSV:
    """ This class convert Supplier CSV file to WooCommerce CSV file """

    def __init__(self, csv_file: str, template: str):
        self._csv_file: str = csv_file
        self._template: str = template
        self._supplier_df: Optional[pd.DataFrame] = None
        self._supplier_records: List[dict] = []
        self._woocommerce_df: Optional[pd.DataFrame] = None
        self._woocommerce_records: List[dict] = []

    def process_supplier_csv(self):
        """ Process supplier csv file and use it to render the template """
        # Previously for brema, we have used "cp1252"
        # Input encoding "cp437" is working fine for both brema, bromic
        self._supplier_df = pd.read_csv(
            self._csv_file,
            header=0,
            encoding="cp437",
            na_filter=False
        )
        self._supplier_records = self._supplier_df.to_dict("records")

    def convert(self):
        """ Convert supplier CSV to WooCommerce CSV"""
        counter = 0
        self.process_supplier_csv()
        for record in self._supplier_records:
            output = Template.render(template=self._template, record=record)
            output = output.replace("\r\n", "  ")
            try:
                if output:
                    self._woocommerce_records.append(yaml.full_load(output))
            except Exception as err:
                print(err)
                print(output)
                counter += 1
        print(f"No of products with wrong syntax: {counter}")

    def save_to_csv(self, output_csv):
        """ Save the woocommerce data to csv """
        self._woocommerce_df = pd.DataFrame(self._woocommerce_records)
        self._woocommerce_df.to_csv(output_csv, index=False)

    @property
    def product_records(self) -> List[Dict]:
        """ Return product records """
        return self._woocommerce_records


if __name__ == "__main__":
    # obj = SupplierCSV2WoocommerceCSV(
    #     csv_file="/Users/dibyaranjan/Upwork/client_nick_woocommerce/brema.csv",
    #     template="brema.yml",
    # )
    # obj.convert()
    # obj.save_to_csv("/tmp/test_brema.csv")

    obj = SupplierCSV2WoocommerceCSV(
        csv_file="/Users/dibyaranjan/Upwork/client_nick_woocommerce/bromic.csv",
        template="bromic.yml"
    )
    obj.convert()
    obj.save_to_csv("/tmp/test_bromic.csv")
