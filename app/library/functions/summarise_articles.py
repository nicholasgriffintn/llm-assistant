from pathlib import Path
from alive_progress import alive_bar

from ..helpers import generate_and_check, get_report_template, logger

def summarise_articles(article_name, summaries, ollama_options, model_name):
    """
    Summarise multiple articles and generate a combined report.

    Args:
        article_name (str): The name of the article.
        summaries (list): List of summaries to combine.
        ollama_options (dict): Options for the ollama model.
        model_name (str): The name of the model to use.
    """

    logger.info(f"Summarising articles into a report: {article_name}")

    report_template = get_report_template("prompts/prompt-report.txt")

    if not report_template:
        return

    combined_summaries = "###\n".join(summaries)

    with alive_bar() as bar:
        try:
            report = generate_and_check(
                report_template.format(docs=combined_summaries),
                ollama_options,
                model_name,
                combined_summaries
            )
            if report:
                encoded_model_name = model_name.replace("/", "_").replace("@", "_")
                output_path = Path(f"{article_name}.report.{encoded_model_name}.md")
                output_path.write_text(report, encoding="utf-8")
                logger.info(f"Report successfully generated and saved to {output_path}")
            else:
                logger.error("Failed to generate a valid report after multiple attempts.")
        except Exception as e:
            logger.error(f"Error during report generation: {e}")
        bar()

    logger.info(f"Finished. Generated report.")

    return report
