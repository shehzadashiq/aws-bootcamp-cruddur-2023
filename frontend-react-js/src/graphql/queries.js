/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getCrdDdbDynamoDBTable1NK2LU7KGZSIP = /* GraphQL */ `
  query GetCrdDdbDynamoDBTable1NK2LU7KGZSIP($pk: String!) {
    getCrdDdbDynamoDBTable1NK2LU7KGZSIP(pk: $pk) {
      message_group_uuid
      pk
      sk
      __typename
    }
  }
`;
export const listCrdDdbDynamoDBTable1NK2LU7KGZSIPS = /* GraphQL */ `
  query ListCrdDdbDynamoDBTable1NK2LU7KGZSIPS(
    $filter: TableCrdDdbDynamoDBTable1NK2LU7KGZSIPFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listCrdDdbDynamoDBTable1NK2LU7KGZSIPS(
      filter: $filter
      limit: $limit
      nextToken: $nextToken
    ) {
      items {
        message_group_uuid
        pk
        sk
        __typename
      }
      nextToken
      __typename
    }
  }
`;
