from pathlib import Path
from alive_progress import alive_bar

from ..helpers import generate, check_summary, logger

def summarise_articles(source, summaries, ollama_options, model_name):
    """
    Summarise multiple articles and generate a combined report.

    Args:
        source (str): The name of the article.
        summaries (list): List of summaries to combine.
        ollama_options (dict): Options for the ollama model.
        model_name (str): The name of the model to use.
    """
    report_template_path = Path("prompts/prompt-report.txt")
    try:
        report_template = report_template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.error(f"Template file not found: {report_template_path}")
        return
    except IOError as e:
        logger.error(f"Error reading template file: {e}")
        return

    combined_summaries = "###\n".join(summaries)
    report_ok = False
    retries = 5
    attempts = 0

    with alive_bar() as bar:
        while not report_ok and retries > 0:
            attempts += 1
            try:
                report = generate(
                    report_template.format(docs=combined_summaries),
                    ollama_options,
                    model_name
                )
                report_ok = check_summary(report, combined_summaries)
                if report_ok:
                    output_path = Path(f"{source}.report.{model_name}.md")
                    output_path.write_text(report, encoding="utf-8")
                    logger.info(f"Report successfully generated and saved to {output_path}")
                else:
                    logger.warning(f"Report generation failed. Retries left: {retries - 1}")
                    retries -= 1
            except Exception as e:
                logger.error(f"Error during report generation: {e}")
                retries -= 1
            bar()

        if not report_ok:
            logger.error("Failed to generate a valid report after multiple attempts.")

    logger.info(f"Finished. Generated report in {attempts} total attempts.")

    return report
