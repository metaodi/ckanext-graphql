# -*- coding: utf-8 -*-
import nose
import json

from ckantoolkit.tests import helpers, factories

eq_ = nose.tools.eq_
assert_true = nose.tools.assert_true


class TestEndpoints(helpers.FunctionalTestBase):

    def test_graphiql_endpoint(self):

        dataset = factories.Dataset(
            notes='Test dataset'
        )

        headers = {'Accept': 'text/html'}
        url = '/graphql'

        app = self._get_test_app()
        response = app.get(url, headers=headers)

        assert 'GraphiQL' in response

    def test_graphql_endpoint(self):

        url = '/graphql'

        app = self._get_test_app()
        res = app.get(url, status=400)
        response = json.loads(res.body)

        assert 'errors' in response
        errors = response['errors']
        eq_(errors[0]['message'], 'Must provide query string.')

    def test_graphql_query(self):

        dataset = factories.Dataset(
            notes='Test dataset'
        )

        url = '/graphql?query={hello}'

        app = self._get_test_app()
        res = app.get(url)
        response = json.loads(res.body)

        assert 'data' in response
        eq_(response['data'], {'hello', 'world'})
