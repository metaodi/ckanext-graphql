# -*- coding: utf-8 -*-
import nose

from ckantoolkit.tests import helpers, factories

eq_ = nose.tools.eq_
assert_true = nose.tools.assert_true


class TestEndpoints(helpers.FunctionalTestBase):

    def test_graphiql_endpoint(self):

        dataset = factories.Dataset(
            notes='Test dataset'
        )

        url = '/graphql'

        app = self._get_test_app()

        response = app.get(url)

        assert 'GraphiQL' in response
