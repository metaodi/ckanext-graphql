# ckanext-graphql

[![Build Status](https://travis-ci.org/metaodi/ckanext-graphql.svg?branch=master)](https://travis-ci.org/metaodi/ckanext-graphql)

**The extension is still in development and not yet ready for production use.**

Requirement: CKAN >= 2.7

This extension aims to provide a [GraphQL](http://graphql.org/) endpoint to query the CKAN.
In the future, it might be considered an alternative to the [CKAN Action API](http://docs.ckan.org/en/latest/api/#action-api-reference).

## Installation

1.  Install the extension on your virtualenv:

        (pyenv) $ pip install -e git+https://github.com/metaodi/ckanext-graphql.git#egg=ckanext-graphql

1.  Install the extension requirements:

        (pyenv) $ pip install -r ckanext-graphql/requirements.txt

1.  Enable the required plugins in your ini file:

        ckan.plugins = graphql


Once the `graphql` plugin is loaded, a new endpoint `/graphql` is available on your CKAN instance.

By default, it serves [GraphiQL](https://github.com/graphql/graphiql), an in-browser _IDE_ to create GraphQL queries.

The endpoint `/graphql` can be directly called with GraphQL-queries.

## Example queries

Query all packages incl. groups and organization:

```
{
  packages {
    name
    ckanId
    organization {
      name
    }
    groups {
      edges {
        group: node {
          name
        }
      }
    }
  }
}
```

# TODO

- [ ] Support all/more models
- [ ] Add support for [Relay](https://facebook.github.io/relay/)
- [ ] Add possibility for mutations
- [ ] Check if data should be read from Solr
- [ ] Add interface to change schema from other CKAN extensions (i.e. add own models)
- [ ] Support custom schemas from [ckanext-scheming](https://github.com/ckan/ckanext-scheming)
- [x] Add travis build
