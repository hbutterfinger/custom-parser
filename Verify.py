import Parser as p
import Test
import traceback


class Verifier:
    def run_test(self, test_name, test_input, expected_output):
        """
        This function runs the lexer and parser on the test input,
        compares the AST with the expected output.
        Returns True if the test passes, False otherwise.
        """
        print(f"--- Running {test_name} ---")
        try:
            # Initialize the lexer and tokenize the input
            lexer = p.Lexer(test_input)
            tokens = lexer.tokenize()

            # Initialize the parser and generate the AST
            parser = p.Parser(tokens)
            ast = parser.parse()
            ast_string = ast.to_string()

            # Remove all spaces and newlines for a clean comparison
            ast_string_clean = self.clean_string(ast_string)
            expected_output_string_clean = self.clean_string(expected_output)

            # Compare the result with the expected output
            if ast_string_clean == expected_output_string_clean:
                print(f"{test_name} passed.\n")
                return True
            else:
                print(f"{test_name} failed.\n")
                print("Wrong AST:")
                print(ast_string_clean)
                return False
        except Exception as e:
            print(f"{test_name} failed with an exception: {e}")
            traceback.print_exc()
            print("--------------------")
            return False

    def clean_string(self, s: str) -> str:
        """
        Utility function to clean a string by removing spaces and newlines.
        """
        return s.replace(" ", "").replace("\n", "")


if __name__ == "__main__":
    verifier = Verifier()
    test_cases = [
        ("Test Case 1", Test.test_input_1, Test.expected_output_1),
        ("Test Case 2", Test.test_input_2, Test.expected_output_2),
        ("Test Case 3", Test.test_input_3, Test.expected_output_3),
        ("Test Case 4", Test.test_input_4, Test.expected_output_4),
        ("Test Case 5", Test.test_input_5, Test.expected_output_5),
        ("Test Case 6", Test.test_input_6, Test.expected_output_6),
        ("Test Case 7", Test.test_input_7, Test.expected_output_7),
        ("Test Case 8", Test.test_input_8, Test.expected_output_8),
        ("Test Case 9", Test.test_input_9, Test.expected_output_9),
        ("Test Case 10", Test.test_input_10, Test.expected_output_10),
        ("Test Case 11", Test.test_input_11, Test.expected_output_11),
        ("Test Case 12", Test.test_input_12, Test.expected_output_12),
    ]

    # Run each test case
    for test_name, test_input, expected_output in test_cases:
        verifier.run_test(test_name, test_input, expected_output)
