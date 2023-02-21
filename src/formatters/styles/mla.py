"""
Стиль цитирования по MLA 9th
"""
from string import Template

from pydantic import BaseModel

from formatters.models import (
    BookModel,
    InternetResourceModel,
    MagazineArticleModel,
    AbstractModel,
)
from formatters.styles.base import BaseCitationStyle
from logger import get_logger

logger = get_logger(__name__)


class MLAAbstract(BaseCitationStyle):
    """
    Форматирование для автореферата к диссертации по MLA.
    """

    data: AbstractModel

    @property
    def template(self) -> Template:
        return Template(
            '$authors Abstract of "$dissertation_title." $field, p. $pages, $year.'
        )

    def substitute(self) -> str:
        logger.info(
            '[MLA] Форматирование автореферата к диссертации "%s" ...',
            self.data.dissertation_title,
        )

        return self.template.substitute(
            authors=self.data.authors,
            dissertation_title=self.data.dissertation_title,
            degree=self.data.degree,
            field=self.data.field,
            specialty_code=self.data.specialty_code,
            city=self.data.city,
            year=self.data.year,
            pages=self.data.pages,
        )


class MLAMagazineArticle(BaseCitationStyle):
    """
    Форматирование для статей из журналов по MLA.
    """

    data: MagazineArticleModel

    @property
    def template(self) -> Template:
        return Template(
            '$authors "$article_title." $magazine_title, no. $magazine_number, $year, pp. $pages.'
        )

    def substitute(self) -> str:
        logger.info(
            '[MLA] Форматирование статьи из журнала "%s" ...', self.data.article_title
        )

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            magazine_title=self.data.magazine_title,
            year=self.data.year,
            magazine_number=self.data.magazine_number,
            pages=self.data.pages,
        )


class MLABook(BaseCitationStyle):
    """
    Форматирование для книг по MLA.
    """

    data: BookModel

    @property
    def template(self) -> Template:
        return Template('$authors "$title." $city, $publishing_house, $year.')

    def substitute(self) -> str:
        logger.info('[MLA] Форматирование книги "%s" ...', self.data.title)

        return self.template.substitute(
            authors=self.data.authors,
            title=self.data.title,
            edition=self.get_edition(),
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )

    def get_edition(self) -> str:
        """
        Получение отформатированной информации об издательстве.

        :return: Информация об издательстве.
        """

        return f"{self.data.edition} изд. – " if self.data.edition else ""


class MLAInternetResource(BaseCitationStyle):
    """
    Форматирование для интернет-ресурсов по MLA.
    """

    data: InternetResourceModel

    @property
    def template(self) -> Template:
        return Template('"$article." $website, $link.')

    def substitute(self) -> str:
        logger.info('[MLA] Форматирование интернет-ресурса "%s" ...', self.data.article)

        return self.template.substitute(
            article=self.data.article,
            website=self.data.website,
            link=self.data.link,
            access_date=self.data.access_date,
        )


class MLACitationFormatter:
    """
    Базовый класс для итогового форматирования списка источников по MLA.
    """

    formatters_map = {
        BookModel.__name__: MLABook,
        InternetResourceModel.__name__: MLAInternetResource,
        MagazineArticleModel.__name__: MLAMagazineArticle,
        AbstractModel.__name__: MLAAbstract,
    }

    def __init__(self, models: list[BaseModel]) -> None:
        """
        Конструктор.

        :param models: Список объектов для форматирования
        """

        formatted_items = []
        for model in models:
            try:
                formatted_items.append(self.formatters_map.get(type(model).__name__)(model))  # type: ignore
            except:
                pass

        self.formatted_items = formatted_items

    def format(self) -> list[BaseCitationStyle]:
        """
        Форматирование списка источников.

        :return:
        """

        return sorted(self.formatted_items, key=lambda item: item.formatted)
