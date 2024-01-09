import django_filters
from django.db.models import Q
from django.db.models.functions import Concat

from application.models import Customer, User


class UserFilter(django_filters.FilterSet):
    """システムユーザのfilter"""

    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = User
        fields = {
            "username": ["contains"],
            "email": ["contains"],
        }


class CustomerFilter(django_filters.FilterSet):
    """お客様のfilter"""

    name = django_filters.CharFilter(method="search_name")
    address = django_filters.CharFilter(method="search_address")

    class Meta:
        model = Customer
        fields = {
            "birthday": ["exact"],
            "email": ["contains"],
            "phone_no": ["startswith"],
        }

    def search_name(self, queryset, name, value):
        """

        Args:
            queryset
            name
            value

        Returns:
            queryset: customerから取得したnameもしくはkanaに該当するqueryset
        """
        return queryset.filter(
            Q(name__contains=value) | Q(kana__contains=value)
        )

    def search_address(self, queryset, address, value):
        """address_queryで取得した住所に該当するquerysetを取得
        Args:
            queryset
            address
        Returns:
            queryset: addressから取得した都道府県・市区町村・番地・その他に該当するqueryset
        """
        return queryset.annotate(
            customer_address=Concat(
                "address__prefecture",
                "address__municipalities",
                "address__house_no",
                "address__post_no",
                "address__other",
            )
        ).filter(customer_address__icontains=value)
