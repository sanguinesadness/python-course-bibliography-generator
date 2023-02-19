"""
Стиль цитирования по ГОСТ Р 7.0.5-2008.
"""
from string import Template

from pydantic import BaseModel

from formatters.models import (
    BookModel,
    InternetResourceModel,
    ArticlesCollectionModel,
    MagazineArticleModel,
    AbstractModel,
)
from formatters.styles.base import BaseCitationStyle
from logger import get_logger

logger = get_logger(__name__)


class GOSTAbstract(BaseCitationStyle):
    """
    Форматирование для автореферата к диссертации по ГОСТу.
    """

    data: AbstractModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $dissertation_title: автореф. дис. ... $degree: $specialty_code. $field $city, $year. $pages с."
        )

    def substitute(self) -> str:
        logger.info(
            '[ГОСТ] Форматирование автореферата к диссертации "%s" ...',
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


class GOSTMagazineArticle(BaseCitationStyle):
    """
    Форматирование для статей из журналов по ГОСТу.
    """

    data: MagazineArticleModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title // $magazine_title. $year. №$magazine_number. $pages."
        )

    def substitute(self) -> str:
        logger.info(
            '[ГОСТ] Форматирование статьи из журнала "%s" ...', self.data.article_title
        )

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            magazine_title=self.data.magazine_title,
            year=self.data.year,
            magazine_number=self.data.magazine_number,
            pages=self.data.pages,
        )


class GOSTBook(BaseCitationStyle):
    """
    Форматирование для книг по ГОСТу.
    """

    data: BookModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $title. – $edition$city: $publishing_house, $year. – $pages с."
        )

    def substitute(self) -> str:
        logger.info('[ГОСТ] Форматирование книги "%s" ...', self.data.title)

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


class GOSTInternetResource(BaseCitationStyle):
    """
    Форматирование для интернет-ресурсов по ГОСТу.
    """

    data: InternetResourceModel

    @property
    def template(self) -> Template:
        return Template(
            "$article // $website URL: $link (дата обращения: $access_date)."
        )

    def substitute(self) -> str:
        logger.info(
            '[ГОСТ] Форматирование интернет-ресурса "%s" ...', self.data.article
        )

        return self.template.substitute(
            article=self.data.article,
            website=self.data.website,
            link=self.data.link,
            access_date=self.data.access_date,
        )


class GOSTCollectionArticle(BaseCitationStyle):
    """
    Форматирование для статьи из сборника по ГОСТу.
    """

    data: ArticlesCollectionModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title // $collection_title. – $city: $publishing_house, $year. – С. $pages."
        )

    def substitute(self) -> str:
        logger.info(
            '[ГОСТ] Форматирование сборника статей "%s" ...', self.data.article_title
        )

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            collection_title=self.data.collection_title,
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )


class GOSTCitationFormatter:
    """
    Базовый класс для итогового форматирования списка источников по ГОСТу.
    """

    formatters_map = {
        BookModel.__name__: GOSTBook,
        InternetResourceModel.__name__: GOSTInternetResource,
        ArticlesCollectionModel.__name__: GOSTCollectionArticle,
        MagazineArticleModel.__name__: GOSTMagazineArticle,
        AbstractModel.__name__: GOSTAbstract,
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
