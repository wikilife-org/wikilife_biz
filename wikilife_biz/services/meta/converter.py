# coding=utf-8


class ConverterException(Exception):
    pass


class Converter(object):
    """
    Converts Model Objects to DTOs
    """

    def _base_node_to_dto(self, node):
        dto = {}
        dto["type"] = node.element_type
        dto["id"] = node._id
        dto["origId"] = node.orig_id
        dto["name"] = node.name
        return dto

    def meta_node_to_dto(self, node):
        dto = self._base_node_to_dto(node)
        dto["otherNames"] = node.other_names
        return dto

    def meta_node_with_metrics_to_dto(self, node, metrics):
        dto = self.meta_node_to_dto(node)
        dto["metrics"] = self.metric_node_list_to_dto(metrics)
        return dto

    def metric_node_to_dto(self, node):
        dto = self._base_node_to_dto(node)

        if node.element_type == "NumericMetricNode":
            dto["min"] = node.min
            dto["max"] = node.max
            dto["default"] = node.default
            dto["unit"] = node.unit
            dto["precision"] = node.precision

        elif node.element_type == "TextMetricNode":
            dto["options"] = node.options
            dto["default"] = node.default

        else:
            raise ConverterException("Unknown Metric node type: %s" %node.element_type)

        return dto

    def meta_node_list_to_dto(self, nodes):
        dto = []

        for node in nodes:
            dto.append(self.meta_node_to_dto(node))

        return dto

    def metric_node_list_to_dto(self, nodes):
        dto = []

        for node in nodes:
            dto.append(self.metric_node_to_dto(node))

        return dto
