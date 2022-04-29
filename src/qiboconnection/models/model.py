""" Generic Model module with CRUD operations """

from abc import ABC
from dataclasses import dataclass, field
from typing import List, cast

from qiboconnection.connection import Connection
from qiboconnection.util import (
    HttpPaginatedData,
    get_last_and_next_page_number_from_links,
)


@dataclass
class Model(ABC):
    """Class to manage CRUD operations with general structures
    that require data model Create, Read, Update, Delete operations
    """

    connection: Connection
    collection_name: str = field(init=False)  # to be defined in the inheritance hierarchy

    def create(self, data: dict, path: str | None = None) -> dict:
        """Creates a new data model by calling a remote API
        Args:
            data (dict): dictionary containing the data.
        Returns:
            dict: returning the created dictionary data
        """
        response, _ = self.connection.send_post_auth_remote_api_call(
            path=path if path is not None else self.collection_name, data=data
        )
        return cast(dict, response)

    def read(self, model_id: int | None = None, path: str | None = None) -> dict:
        """Gets the object with the given model_id by calling a remote API
        Args:
            model_id (int): model identifier
        Returns:
            dict: data in a dictionary format
        """
        if model_id is None and path is None:
            raise AttributeError("Either 'model_id' or 'path' MUST be defined.")

        response, _ = self.connection.send_get_auth_remote_api_call(
            path=path if path is not None else f"{self.collection_name}/{model_id}"
        )
        return cast(dict, response)

    def update(self, data: dict, model_id: int | None = None, path: str | None = None) -> dict:
        """Updates the specified object with the given data by calling a remote API

        Args:
            model_id (int): model identifier
            data (dict): dictionary containing the data.
        Returns:
            dict: returning the updated dictionary data
        """
        if model_id is None and path is None:
            raise AttributeError("Either 'model_id' or 'path' MUST be defined.")

        response, _ = self.connection.send_put_auth_remote_api_call(
            path=path if path is not None else f"{self.collection_name}/{model_id}", data=data
        )
        return cast(dict, response)

    def delete(self, model_id: int | None = None, path: str | None = None) -> None:
        """Deletes the object with the given model_id by calling a remote gateway

        Args:
            model_id (int): model identifier
        """
        if model_id is None and path is None:
            raise AttributeError("Either 'model_id' or 'path' MUST be defined.")

        self.connection.send_delete_auth_remote_api_call(
            path=path if path is not None else f"{self.collection_name}/{model_id}"
        )

    def list_elements(self) -> List[dict]:
        """List all elements by calling a remote API

        Returns:
            List[dict]: Return all elements
        """
        response, _ = self.connection.send_get_auth_remote_api_call(path=self.collection_name)
        paginated_data = HttpPaginatedData(data=response)

        return self._get_all_elements(accumulated_items=paginated_data.items, paginated_data=paginated_data)

    def _get_all_elements(self, accumulated_items: List[dict], paginated_data: HttpPaginatedData) -> List[dict]:
        """Get all elements from a paginated Http response querying the API until there is no elements left

        Args:
            accumulated_items (List[dict]): Items already retrieved from the API
            paginated_data (HttpPaginatedData): First paginated_data

        Returns:
            List[dict]: all elements as a list
        """
        accumulated_items += paginated_data.items
        last_page, next_page = get_last_and_next_page_number_from_links(
            self_link=paginated_data.self, next_link=paginated_data.links.next
        )

        if paginated_data.total == len(paginated_data.items) or last_page == next_page:
            return accumulated_items

        response, _ = self.connection.send_get_auth_remote_api_call(
            path=f"{self.collection_name}?page={next_page}&per_page{paginated_data.per_page}"
        )
        paginated_data = HttpPaginatedData(data=response)
        return self._get_all_elements(accumulated_items=paginated_data.items, paginated_data=paginated_data)
