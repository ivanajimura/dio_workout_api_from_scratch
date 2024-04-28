class InputValidator:
    @staticmethod
    def is_valid_cpf(cpf: str|int) -> bool:
        # Removing non-numeric characters from the string
        cpf = ''.join(filter(str.isdigit, cpf))

        # Checking if the CPF has 11 digits
        if len(cpf) != 11:
            return False

        # Calculating the first verifier digit
        total = sum(int(cpf[i]) * (10 - i) for i in range(9))
        remainder = total % 11
        verifier1 = 0 if remainder < 2 else 11 - remainder

        # Calculating the second verifier digit
        total = sum(int(cpf[i]) * (11 - i) for i in range(10))
        remainder = total % 11
        verifier2 = 0 if remainder < 2 else 11 - remainder

        # Checking if the verifier digits match the CPF
        if int(cpf[9]) != verifier1 or int(cpf[10]) != verifier2:
            return False

        return True
    
    @staticmethod
    def is_length_within_max(input: any, max_length: int = 0) -> bool:
        if len(input) <= max_length:
            return True
        return False

    @staticmethod
    def is_length_higher_or_equal_to_min(input: any, min_length: int = 0) -> bool:
        if len(input) >= min_length:
            return True
        return False
    
    @staticmethod
    def is_length_acceptable(input: any, max_length: int = 0, min_length: int = 0) -> bool:
        return InputValidator.is_length_within_max(input, max_length) and InputValidator.is_length_higher_or_equal_to_min(input, min_length)

    @staticmethod
    def is_input_in_list(input: any, options: list[any]) -> bool:
        return input in options







