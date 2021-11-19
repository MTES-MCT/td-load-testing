me_query = """
    query {
        me {
            id
            companies	{
                siret
                name
            }
        }
    }
"""
bsd_query = """
     query GetBsds( $siret: String!) {
  bsds(where: { #tab: [$siret] }) {
    edges {
      node {
        ... on Form {
             id
                customId
                sentAt
                emitter {
                  company {
                    siret
                  }
                }
                emitter {
                  type
                  workSite {
                    name
                    address
                    city
                    postalCode
                    infos
                  }
                  company {
                    name
                    siret
                    address
                    contact
                    country
                    phone
                    mail
                  }
                }
                recipient {
                  cap
                  processingOperation
                  isTempStorage
                  company {
                    name
                    siret
                    address
                    contact
                    country
                    phone
                    mail
                  }
                }
                transporter {
                  isExemptedOfReceipt
                  receipt
                  department
                  validityLimit
                  numberPlate
                  company {
                    name
                    siret
                    address
                    contact
                    country
                    phone
                    mail
                  }
                }
                trader {
                  receipt
                  department
                  validityLimit
                  company {
                    name
                    siret
                    address
                    contact
                    country
                    phone
                    mail
                  }
                }
                broker {
                  receipt
                  department
                  validityLimit
                  company {
                    name
                    siret
                    address
                    contact
                    country
                    phone
                    mail
                  }
                }
                wasteDetails {
                  code
                  name
                  onuCode
                  packagingInfos {
                    type
                    other
                    quantity
                  }
                  quantity
                  consistence
                  pop
                }
                appendix2Forms {
                  id
                  readableId
                }
                ecoOrganisme {
                  name
                  siret
                } 
        
        }
        ... on Bsdasri {
          id
          dasristatus: status
            isDraft
            
               emitter {
          company {
            siret
        
          }
     
          emission {
            packagings {
              type
              other
              quantity
              volume
            }
            weight {
              value
              isEstimate
            }

            signature {
              author
              date
            }
          }
        }
              transporter {
          company {
            siret
          }

          recepisse {
            number
            department
            validityLimit
          }
          transport {
            handedOverAt
            takenOverAt
            mode

            volume
            weight {
              value
              isEstimate
            }
            packagings {
              type
              other
              quantity
              volume
            }

            acceptation {
              status
              refusalReason

              refusedWeight
            }
         
          }
        }
          destination {
          company {
            siret
            name
    
          }
          reception {
            date

            volume

            acceptation {
              status
              refusalReason
              refusedWeight
            }
         
          }
          operation {
            date
            code
          
          }
        }
            createdAt
        updatedAt
        }
        ... on Bsvhu {
        id
        isDraft
        identification {
          numbers
          type
        }

        emitter {
          agrementNumber
          company {
            siret
          }
        }

        transporter {
          company {
            siret
            name
            address
            contact
            mail
            phone
            vatNumber
          }
          recepisse {
            number
          }
        }
        destination {
          type
          agrementNumber
          company {
            siret
            name
            address
            contact
            mail
            phone
            vatNumber
          }
          plannedOperationCode
          reception {
            date

            quantity

            weight

            acceptationStatus

            refusalReason
          }
          operation {
            date
            code
          }
        }
        weight {
          value
        }
      }
          
        ... on Bsff {
          id
          bsffStatus: status
          bsffEmitter: emitter {
            company {
              siret
              name
            }
          }
          bsffTransporter: transporter {
              company {
                siret
                name
              }
            }
            bsffDestination: destination {
              company {
                siret
                name
              }
            }
            waste {
              code
              description
            }
        }
        ... on Bsda {
          id

          emitter {
            company {
              siret
            }
          }
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
    totalCount
  }
}

"""

base_form_query = """
query Forms($siret: String){
  forms(siret: $siret) {
    id
    readableId
    emitter {
      company {
        siret
      }
    }
    transporter {
      company {
        siret
      }
    }
    recipient {
      company {
        siret
      }
    }
    wasteDetails {
      code
      name
      onuCode
      packagingInfos {
        type
        other
        quantity
      }
      quantity
      quantityType
      consistence
    }
  }
}
"""

base_dasri_query = """
query {
  bsdasris  {
    edges {
      node {
        id
        status
        type

        waste {
          code
          adr

        }

        emitter {
          company {
            siret
            name
            address
            country
            contact
            phone
            mail
          }
          pickupSite {
            name
            address
            postalCode
            infos
          }
          emission {
            packagings {
              type
              other
              quantity
              volume
            }
            weight {
              value
              isEstimate
            }

            signature {
              author
              date
            }
          }
        }

        isDraft

        transporter {
          company {
            siret
          }

          recepisse {
            number
            department
            validityLimit
          }
          transport {
            handedOverAt
            takenOverAt
            mode

            volume
            weight {
              value
              isEstimate
            }
            packagings {
              type
              other
              quantity
              volume
            }

            acceptation {
              status
              refusalReason

              refusedWeight
            }
            signature {
              author
              date
            }
          }
        }

        destination {
          company {
            siret
            name
            address
            country
            contact
            phone
            mail
          }
          reception {
            date

            volume

            acceptation {
              status
              refusalReason
              refusedWeight
            }
            signature {
              author
              date
            }
          }
          operation {
            date
            code
            signature {
              author
              date
            }
          }
        }

        createdAt
        updatedAt

      }
    }
  }
}

"""

light_dasri_query = """
query {
  bsdasris  {
    edges {
      node {
        id
        status
        type

        waste {
          code
          adr

        }

        emitter {
          company {
            siret
        
          }
     
          emission {
            packagings {
              type
              other
              quantity
              volume
            }
            weight {
              value
              isEstimate
            }

            signature {
              author
              date
            }
          }
        }

        isDraft

        transporter {
          company {
            siret
          }

          recepisse {
            number
            department
            validityLimit
          }
          transport {
            handedOverAt
            takenOverAt
            mode

            volume
            weight {
              value
              isEstimate
            }
            packagings {
              type
              other
              quantity
              volume
            }

            acceptation {
              status
              refusalReason

              refusedWeight
            }
         
          }
        }

        destination {
          company {
            siret
            name
    
          }
          reception {
            date

            volume

            acceptation {
              status
              refusalReason
              refusedWeight
            }
         
          }
          operation {
            date
            code
          
          }
        }

        createdAt
        updatedAt

      }
    }
  }
}

"""

group_dasri_query = """
query {
  bsdasris  {
    edges {
      node {
        id
        status
        type

        waste {
          code
          adr

        }

        emitter {
          company {
            siret
            name
            address
            country
            contact
            phone
            mail
          }
          pickupSite {
            name
            address
            postalCode
            infos
          }
          emission {
            packagings {
              type
              other
              quantity
              volume
            }
            weight {
              value
              isEstimate
            }

            signature {
              author
              date
            }
          }
        }

        isDraft

        transporter {
          company {
            siret
          }

          recepisse {
            number
            department
            validityLimit
          }
          transport {
            handedOverAt
            takenOverAt
            mode

            volume
            weight {
              value
              isEstimate
            }
            packagings {
              type
              other
              quantity
              volume
            }

            acceptation {
              status
              refusalReason

              refusedWeight
            }
            signature {
              author
              date
            }
          }
        }

        destination {
          company {
            siret
            name
            address
            country
            contact
            phone
            mail
          }
          reception {
            date

            volume

            acceptation {
              status
              refusalReason
              refusedWeight
            }
            signature {
              author
              date
            }
          }
          operation {
            date
            code
            signature {
              author
              date
            }
          }
        }

        createdAt
        updatedAt

        grouping {
          id
          quantity
          volume
          weight
          takenOverAt
          postalCode
        }
        groupedIn {
          id
          emitter {
            company {
              siret
            }
          }
        }
      }
    }
  }
}

"""


base_vhu_query = """
 query GetBsvhus {
  bsvhus {
    edges {
      node {
        id
        isDraft
        identification {
          numbers
          type
        }

        emitter {
          agrementNumber
          company {
            siret
          }
        }

        transporter {
          company {
            siret
            name
            address
            contact
            mail
            phone
            vatNumber
          }
          recepisse {
            number
          }
        }
        destination {
          type
          agrementNumber
          company {
            siret
            name
            address
            contact
            mail
            phone
            vatNumber
          }
          plannedOperationCode
          reception {
            date

            quantity

            weight

            acceptationStatus

            refusalReason
          }
          operation {
            date
            code
          }
        }
        weight {
          value
        }
      }
    }
  }
}


"""
base_bsff_query = """
query Bsffs {
  bsffs {
    edges {
      node {
        id
        isDraft
        createdAt
        updatedAt
        status
        type
        emitter {
          customInfo
          company {
            siret
            name
            address
            country
            contact
            phone
            mail
          }
          emission {
            signature {
              author
              date
            }
          }
        }
        packagings {
          name
          volume
          numero
          weight
        }
        waste {
          code
          description
          adr
        }
        weight {
          value
          isEstimate
        }
        transporter {
          customInfo
          company {
            siret
            name
            address
            country
            contact
            phone
            mail
          }
          recepisse {
            number
            department
            validityLimit
          }
          transport {
            mode
            signature {
              author
              date
            }
          }
        }
        destination {
          customInfo
          company {
            siret
            name
            address
            country
            contact
            phone
            mail
          }
          cap
          plannedOperationCode
          reception {
            date
            weight
            acceptation {
              status
              refusalReason
            }
            signature {
              date
              author
            }
          }
          operation {
            code
            nextDestination {
              company {
                siret
                name
                address
                country
                contact
                phone
                mail
              }
            }
            signature {
              author
              date
            }
          }
        }

        forwarding {
          id
        }
        forwardedIn {
          id
        }
        repackaging {
          id
        }
        repackagedIn {
          id
        }

        groupedIn {
          id
        }
      }
    }
  }
}


"""


base_bsda_query = """query Bsdas {
  bsdas {
    edges {
      node {
        id
        createdAt
        updatedAt
        isDraft
        status
        type
        emitter {
          isPrivateIndividual
          company {
            name
            siret
            address
            contact
            phone
            mail
          }
          customInfo
          pickupSite {
            name
            address
            city
            postalCode
            infos
          }
          emission {
            signature {
              author
              date
            }
          }
        }
        ecoOrganisme {
          name
          siret
        }
        waste {
          code
          name
          familyCode
          materialName
          consistence
          sealNumbers
          adr
        }
        packagings {
          other
          quantity
          type
        }
        weight {
          isEstimate
          value
        }
        broker {
          company {
            siret
            address
            contact
            phone
            mail
          }
          recepisse {
            number
            department
            validityLimit
          }
        }
        destination {
          company {
            name
            siret
            address
            contact
            phone
            mail
          }
          cap
          plannedOperationCode
          customInfo
          reception {
            date
            weight
            acceptationStatus
            refusalReason
          }
          operation {
            code
            date
            signature {
              author
              date
            }
            nextDestination {
              company {
                siret
                vatNumber
                name
                address
                contact
                phone
                mail
              }
              cap
              plannedOperationCode
            }
          }
        }
        transporter {
          customInfo
          company {
            name
            siret
            address
            contact
            phone
            mail
            vatNumber
          }
          recepisse {
            isExempted
            number
            department
            validityLimit
          }
          transport {
            mode
            plates
            takenOverAt
            signature {
              author
              date
            }
          }
        }
        worker {
          company {
            name
            siret
            address
            contact
            phone
            mail
          }
          work {
            hasEmitterPaperSignature
            signature {
              author
              date
            }
          }
        }
        groupedIn {
          id
        }
        grouping {
          id
        }
        forwarding {
          id
        }
        forwardedIn {
          id
        }
      }
    }
  }
}
"""
formslifecycle_query = """
   query FormsLifeCycle($siret: String){
  formsLifeCycle(siret: $siret){
    statusLogs {
      id
      status
      updatedFields
      loggedAt
      form {
        id
        readableId
      }
      user {
        id
        email
      }
    }
    hasNextPage
    hasPreviousPage
    startCursor
    endCursor
    count
  }
}
"""
