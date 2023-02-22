from django.contrib.admin.filters import (
    SimpleListFilter,
    AllValuesFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter,
    RelatedOnlyFieldListFilter,
)


class SimpleDropdownFilter(SimpleListFilter):
    template = "filters/dropdown_filter.html"


class DropdownFilter(AllValuesFieldListFilter):
    template = "filters/dropdown_filter.html"


class ChoiceDropdownFilter(ChoicesFieldListFilter):
    template = "filters/dropdown_filter.html"


class RelatedDropdownFilter(RelatedFieldListFilter):
    template = "filters/dropdown_filter.html"


class RelatedOnlyDropdownFilter(RelatedOnlyFieldListFilter):
    template = "filters/dropdown_filter.html"
