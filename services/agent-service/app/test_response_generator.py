"""
Test Response Generator.
"""

from pprint import pprint

from app.response.response_generator import (
    ResponseGenerator
)


def main():

    generator = ResponseGenerator()

    sample = {

        "company": "Infosys",

        "stock": {

            "close": 1044.30,

            "change": -0.55

        },

        "sentiment": "Positive"

    }

    response = generator.generate(

        "Summarize Infosys",

        sample

    )

    print()

    print("=" * 80)

    print("Response Generator")

    print("=" * 80)

    print()

    pprint(response)


if __name__ == "__main__":

    main()