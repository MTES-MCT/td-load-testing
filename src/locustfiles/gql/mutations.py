form_create = """
  mutation CreateForm($createFormInput: CreateFormInput!) {
    createForm(createFormInput: $createFormInput) {
      id
      recipient {
        company {
          siret
        }
      }
      emitter {
        workSite {
          name
          address
          city
          postalCode
          infos
        }
      }
      ecoOrganisme {
        siret
      }
      temporaryStorageDetail {
        destination {
          company {
            siret
            name
          }
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
        }
        isExemptedOfReceipt
        receipt
        department
        validityLimit
        numberPlate
        customInfo
      }
      trader {
        company {
          siret
          name
          address
          contact
          mail
          phone
        }
        receipt
        department
        validityLimit
      }
      wasteDetails {
        packagingInfos {
          type
          other
          quantity
        }
      }
      appendix2Forms {
        id
      }
    }
  }
"""
form_update = """
  mutation UpdateForm($updateFormInput: UpdateFormInput!) {
    updateForm(updateFormInput: $updateFormInput) {
      id
      customId
      recipient {
        company {
          siret
        }
      }
      emitter {
        workSite {
          name
          address
          city
          postalCode
          infos
        }
      }
      ecoOrganisme {
        siret
      }
      temporaryStorageDetail {
        destination {
          company {
            siret
            name
          }
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
        }
        isExemptedOfReceipt
        receipt
        department
        validityLimit
        numberPlate
        customInfo
      }
      trader {
        company {
          siret
          name
          address
          contact
          mail
          phone
        }
        receipt
        department
        validityLimit
      }
      wasteDetails {
        packagingInfos {
          type
          other
          quantity
        }
      }
      appendix2Forms {
        id
      }
    }
  }
"""

dasri_create = """
mutation BsdasriCreate($input: BsdasriInput!) {
  createBsdasri(input: $input) {
    id
    waste {
      code
    }
    isDraft
    type

    status
    createdAt
    updatedAt
    ecoOrganisme {
      siret
    }
  }
}

"""
