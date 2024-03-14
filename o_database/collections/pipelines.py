class OriginDBPipelines:

    def _create_match_stage(self, criteria):
        return {"$match": criteria}

    def generate_pipeline(self, criteria):
        match_stage = self._create_match_stage(criteria)
        pipeline = [match_stage]

        return pipeline

    def doc_field_val_startswith(self, doc_attr, field_values: list):
        """
        returns MongoDB filter for aggregation
        it returns the documents that have the field value starting with the inputted :param sel_filter:
        """
        if len(field_values) == 1:
            attr_val = field_values[0]

        else:
            attr_val = ".".join(field_values)

        pipeline = [{"$match": {doc_attr: {"$regex": f"^{attr_val}"}}}]
        return pipeline

    def doc_field_val_matches(self, doc_attr, field_values: list):
        """
        returns MongoDB filter for aggregation
        it returns the documents that have the field value matching exactly with the inputted :param sel_filter:

        Args:
            doc_field:
        """
        if len(field_values) == 1:
            attr_val = field_values[0]

        else:
            attr_val = ".".join(field_values)

        pipeline = [{"$match": {doc_attr: attr_val}}]
        return pipeline
