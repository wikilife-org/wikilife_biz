# coding=utf-8

import math


PAGE_SIZE = 25


class MetaServiceException(Exception):
    pass


class MetaService(object):

    _logger = None
    _meta_dao = None
    _converter = None

    def __init__(self, logger, meta_dao, converter):
        self._logger = logger
        self._meta_dao = meta_dao
        self._converter = converter

    def _get_node_by_id(self, node_id):
        node = self._meta_dao.get_node_by_id(node_id)

        if node == None:
            raise MetaServiceException("node_id %s not found".format(node_id))

        return node

    def get_node_by_id(self, node_id):
        node = self._get_node_by_id(node_id)
        dto = self._converter.meta_node_to_dto(node)
        return dto

    def get_metric_by_id(self, metric_id):
        metric = self._get_node_by_id(metric_id)
        dto = self._converter.metric_node_to_dto(metric)
        dto["measuring"] = self._converter.meta_node_list_to_dto(self._meta_dao.get_nodes_measured_by(metric_id))
        return dto

    def get_node_by_orig_id(self, node_orig_id):
        node = self._meta_dao.get_node_by_orig_id(node_orig_id)

        if node == None:
            raise MetaServiceException("node_orig_id %s not found".format(node_orig_id))

        dto = self._converter.meta_node_to_dto(node)
        return dto

    def get_node_full(self, node_id):
        """
        Returns
        { 
            id: 0,
            orig_id: 0,
            name: "",
            other_names: "",
            is: [{id: 0, name: ""}],
            has: [{id: 0, name: ""}],
            measured_by: [{id: 0, name: ""}],
            measured_by_default: [{id: 0, name: ""}] //More than 1 default metric is a data error
        }
        """
        items, items_total = self._meta_dao.get_children_pag(node_id, skip=0, limit=100)

        dto = self.get_node_by_id(node_id)
        dto["is"] = self._converter.meta_node_list_to_dto(self._meta_dao.get_parent_nodes_by_id(node_id))
        dto["has"] = self._converter.meta_node_list_to_dto(self._meta_dao.get_component_nodes(node_id))
        dto["measuredBy"] = self._converter.metric_node_list_to_dto(self._meta_dao.get_node_metrics(node_id))
        dto["measuredByDefault"] = self._converter.metric_node_list_to_dto(self._meta_dao.get_default_metrics(node_id))
        return dto

    def get_descendants_count(self, node_id):
        return self._meta_dao.get_descendants_count(node_id)

    def get_node_with_metrics(self, node_id):
        node = self._get_node_by_id(node_id)
        metrics = self._meta_dao.get_node_metrics(node_id)
        dto = self._converter.meta_node_with_metrics_to_dto(node, metrics)
        dto["is"] = self._converter.meta_node_list_to_dto(self._meta_dao.get_parent_nodes_by_id(node_id))
        dto["has"] = self._converter.meta_node_list_to_dto(self._meta_dao.get_component_nodes(node_id))
        return dto

    def get_node_parents(self, node_id):
        nodes = self._meta_dao.get_parent_nodes_by_id(node_id)
        dto = self._converter.meta_node_list_to_dto(nodes)
        return dto

    def get_node_ancestors(self, node_id):
        nodes = self._meta_dao.get_ancestors(node_id)
        dto = self._converter.meta_node_list_to_dto(nodes)

        for item in dto:
            item["parentIds"] = self._meta_dao.get_parent_ids_by_id(item["id"])

        return dto

    def get_node_children(self, node_id, page_index=0, page_size=PAGE_SIZE):
        items, items_total = self._meta_dao.get_children_pag(node_id, skip=page_index*page_size, limit=page_size)
        nodes_page_dto = self._create_page(page_index, items_total, self._converter.meta_node_list_to_dto(items), page_size)
        return nodes_page_dto

    def find_nodes(self, node_name, page_index=0):
        items, items_total = self._meta_dao.find_nodes(node_name, skip=page_index*PAGE_SIZE, limit=PAGE_SIZE)
        nodes_page_dto = self._create_page(page_index, items_total, self._converter.meta_node_list_to_dto(items))

        for item in nodes_page_dto["items"]:
            node_id = item["id"]
            #item["parentIds"] = self._meta_dao.get_parent_ids_by_id(node_id)
            #item["is"] = self._converter.meta_node_list_to_dto(self._meta_dao.get_parent_nodes_by_id(node_id))
            #item["has"] = self._converter.meta_node_list_to_dto(self._meta_dao.get_component_nodes(node_id))
            #item["measuredBy"] = self._converter.metric_node_list_to_dto(self._meta_dao.get_node_metrics(node_id))
            #item["measuredByDefault"] = self._converter.metric_node_list_to_dto(self._meta_dao.get_default_metrics(node_id))

        return nodes_page_dto

    def _create_page(self, page_index, items_total, items, page_size=PAGE_SIZE):
        nodes_page = {}
        nodes_page["pageIndex"] = page_index
        nodes_page["pageCount"] = int(math.ceil(items_total*1.0/page_size)) if items_total > 0 else 0
        nodes_page["pageSize"] = page_size
        nodes_page["itemsCount"] = len(items)
        nodes_page["itemsTotal"] = items_total
        nodes_page["itemsFrom"] = page_index * page_size
        nodes_page["itemsTo"] = nodes_page["itemsFrom"] + nodes_page["itemsCount"] -1 
        nodes_page["items"] = items
        return nodes_page
