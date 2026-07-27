from qgen.model_loader import (
    tokenizer_1,
    model_1,
    tokenizer_2,
    model_2
)

from qgen.retriever import (
    retrieve_questions_for_ats
)

from qgen.prompt_builder import (
    build_llm_prompt
)


class QGenEngine:

    def generate_questions(
        self,
        ats_result
    ):

        print(
            "\nSTEP 1 - Retrieving Questions..."
        )

        retrieved = (
            retrieve_questions_for_ats(
                ats_result
            )
        )

        print("\nRETRIEVED DATAFRAME:")
        print(retrieved)
        print(retrieved.columns)

        print(
            "\nSTEP 2 - Building Prompt..."
        )

        prompt = (
            build_llm_prompt(
                ats_result,
                retrieved
            )
        )

        print(
            "\nSTEP 3 - FLAN-T5 Generation..."
        )

        inputs = tokenizer_1(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        outputs = model_1.generate(
            **inputs,
            max_new_tokens=256
        )

        raw_questions = tokenizer_1.decode(
            outputs[0],
            skip_special_tokens=True
        )

        print(
            "\nSTEP 4 - Cleaning Questions..."
        )

        clean_prompt = f"""
Clean and improve:

{raw_questions}
"""

        clean_inputs = tokenizer_2(
            clean_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        clean_outputs = model_2.generate(
            **clean_inputs,
            max_new_tokens=256
        )

        final_questions = tokenizer_2.decode(
            clean_outputs[0],
            skip_special_tokens=True
        )

        # USE RETRIEVED QUESTIONS
        # FLAN output kept only for future research

        questions = retrieved[
            "question_text_clean"
        ].head(5).tolist()

        return {

            "retrieved_count":
            len(retrieved),

            "questions":
            questions,

            "llm_output":
            final_questions
        }