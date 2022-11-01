Feature: SRD074 Setup Reagents
  To verify and validate the List of Reagents screen and Reagent parameters
  verifies:
  1) The menu navigation and "List of Reagent" screen header and column header
  2) Display of parameters, its control type and format.
  3) Default value and the list of values of the parameters
  4) validation of the parameters, soft keys and Headers

  Scenario: 31674_User navigation - Setup - Chemicals - Reagents
    Given I am on the "Menu Tree"
    When I navigate to the "Reagents" via Setup->Chemicals
    Then The "List of Reagents" screen is displayed

  Scenario: 31675_List of Reagents - Screen header
    Given I am on the "List of Reagents" screen
    Then The screen header is displayed as "Reagents"

  Scenario Outline: 31675_List of Reagents - column headers
    Given I am on the "List of Reagents" screen
    Then The column header <header> is in position <order> from left
    Examples:
      | header      | order |
      | Category    | 1     |
      | Name        | 2     |
      | Assigned to | 3     |
      | Connection  | 4     |

  Scenario: 31675_30328_List of Reagents - Display of "New" softkey
    Given I am on the "List of Reagents" screen
    Then The softkey "New" is displayed at position "3"

  Scenario: 31675_30324_List of Reagents - "New" softkey functionality
    Given I am on the "List of Reagents" screen
    When I press the softkey "New"
    Then I am on the "Reagent parameters(Creation)" screen

  Scenario: 31676_46374_Reagent parameter screen(Creation) - screen Header
    Given I am on the "Reagent Parameter(Creation)" screen
    Then The screen header is displayed as "Create: Reagent"

  Scenario Outline: 31676_Reagent parameter screen(Creation) - softkeys verification
    Given I am on the "Reagent Parameter(Creation)" screen
    Then The softkey <softkey> is visible
    #TODO: Not implemented for color verification
    And The softkey <softkey> is in <color>
    And The softkey <softkey> is at position <position>
    Examples:
      | softkey | color | position |
      | Cancel  | Blue  | 1        |
      | Create  | Green | 5        |

  Scenario: 31676_30321(Cancel)Navigation to Reagents list screen from parameter screen
    Given I am on the "Reagent Parameter(Creation)" screen
    When I press the softkey "Cancel"
    Then I am on the "List of Reagents" screen

  Scenario Outline: 31676_46374_Reagent parameter screen(Creation) - parameters - Default values - 'Reagent' tab area
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "Reagent" tab area
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label          | default_value   | control_type | state     | order |
      | Name                 | Blank X         | DataField    | Enabled   | 1     |
      # Have to check for field ID
      | ID                   | empty           | DataField    | Read-only | 2     |
      | Unit                 | mmol            | DataField    | Enabled   | 3     |
      | Value                | 0.0             | DataField    | Enabled   | 4     |
      | Determination method | Manual          | DataField    | Read-only | 5     |
      | Determination date   | Current date    | DataField    | Read-only | 6     |
      | Determined by        | [Logged-in user | DataField    | Read-only | 7     |

  # Parameters for this tab is in Draft state - TBD later
  Scenario Outline: 31676_46374_Reagent parameter screen(Creation) - parameters - Default values - 'Monitoring' tab area
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "Monitoring" tab area
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label | default_value | control_type | state | order |

  # Parameters in this tab are more related to LCM and HR
  Scenario Outline: 31676_46374_Reagent parameter screen(Creation) - parameters - Default values - 'General' tab area
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "General" tab area
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label            | default_value | control_type | state     | order |
      | Internal ID            |               | DataField    | Enabled   | 1     |
      | Version                |               | DataField    | Read-only | 2     |
      | Last modification time |               | DataField    | Enabled   | 3     |
      | Modified by            |               | DataField    | Enabled   | 4     |


  Scenario Outline: 31676_Reagent parameter screen(Creation) - Name - parameter validation
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "Reagent" tab area
    And I am on the keyboard screen displayed for the parameter "Name"
    When I enter the value <input>
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    Examples:
      | input                                                  | accept_reject | validation_msg       |
      | Blank 2                                                | Accepts       | No                   |
      | BlanknameBlanknameBlanknameBlanknameBlanknameBlankname | Rejects       | Value outside limits |
      | Balnk 3                                                | Accepts       | No                   |

  # This parameter applies for LCM
  Scenario: 31676_Reagent parameter screen(Creation) - ID - parameter validation
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "Reagent" tab area
    Then The parameter ID has the value "Value x"

  Scenario Outline: 31676_Reagent parameter screen(Creation) - Unit - parameter validation
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "Reagent" tab area
    And I am on the keyboard screen displayed for the parameter "Unit"
    When I enter the value <input>
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    Examples:
      | input              | accept_reject | validation_msg       |
      | mmmol              | Accepts       | No                   |
      | BlanknameBlankname | Rejects       | Value outside limits |
      | mol                | Accepts       | No                   |

  Scenario Outline: 31676_Reagent parameter screen(Creation) - Value - parameter validation
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "Reagent" tab area
    And I am on the keyboard screen displayed for the parameter "Value"
    When I enter the value <input>
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    Examples:
      | input      | accept_reject | validation_msg       |
      | 10.123456  | Accepts       | No                   |
      | 11.1234567 | Rejects       | Value outside limits |
      | 100.000000 | Accepts       | No                   |

  # Validation of this parameter involves on various other resources defined in multiple SRDs
  Scenario: 31676_Reagent parameter screen(Creation) - Determination method - parameter validation
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "Reagent" tab area
    # TBD the value
    Then The value of the parameter "Determination method" should be Value

  # Validation of this parameter involves on various other resources defined in multiple SRDs
  Scenario: 45609_Reagent parameter screen(Creation) - Determination date - parameter validation
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "Reagent" tab area
    # TBD the value
    Then The value of the parameter "Determination date" should be Value

  # Validation of this parameter involves on various other resources defined in multiple SRDs
  Scenario: 45609_Reagent parameter screen(Creation) - Determined by - parameter validation
    Given I am on the "Reagent Parameter(Creation)" screen
    And I am on "Reagent" tab area
    # TBD the value
    Then The value of the parameter "Determined by" should be Logged-in user

  # Validation of parameters in "Monitoring" tab area - TBD

  # Parameters in the "General" tab area are related to LCM

  Scenario: 45609_30325(Create)_Reagent parameter screen(Creation) - "Create" softkey functionality
    Given I am on the "Reagent Parameter(Creation)" screen
    And All the parameters has valid values
    When I press the softkey "Create"
    Then The new "Reagent" is created
    And The "Reagent parameter screen(Editing)" screen is displayed

  Scenario Outline: 45609_Reagent parameter screen(Editing) - softkeys verification
    Given I am on the "Reagent parameter screen(Editing)" screen
    Then The softkey <softkey> is visible
    And The softkey <softkey> is in <color>
    And The softkey <softkey> is at position <position>
    Examples:
      | softkey | color | position |
      | Back    | Blue  | 1        |
      | Delete  | Blue  | 3        |

  Scenario: 45609_30322(Back)Navigation to Reagents list screen from parameter screen
    Given I am on the "Reagent Parameter(Editing)" screen
    When I press the softkey "Cancel"
    Then I am on the "List of Reagents" screen

  Scenario: 31675_List of Reagents - Selection of existing Reagent
    Given I am on the "List of Reagents" screen
    When I select any Reagent from the list
    Then I am on the "Reagent parameter screen(Editing)" screen

  Scenario Outline: 45609_46374_Reagent parameter screen(Editing) - unsaved changes - sofktkeys verification
    Given I am on the "Reagent parameter screen(Editing)" screen
    When I update any parameter of Reagent with new value
    Then The softkey <softkey> is visible
    And The softkey <softkey> is in <color>
    And The softkey <softkey> is at position <position>
    Examples:
      | softkey | color | position |
      | Discard | Blue  | 1        |
      | Delete  | Blue  | 3        |
      | Save    | Green | 5        |

  Scenario: 45609_30320(Discard)_Reagent parameter screen(Editing)- "Discard Changes" popup
    Given I am on the "Reagent parameter screen(Editing)" screen with updated values
    When I press the softkey "Discard"
    Then The "popup ID 16" displayed on the screen

  Scenario: 45609_Reagent parameter screen(Editing) - "Discard Changes"_"No"
    Given I am on the "popup ID 16"
    When I press "No" in popup
    Then I am on the "Reagent parameter screen(Editing)" screen
    And I have the parameters with updated values

  Scenario: 45609_30323(Delete)_Reagent parameter screen(Editing) - "Delete" popup
    Given I am on the "Reagent parameter screen(Editing)" with updated values
    When I press the softkey "Delete"
    Then The "popup ID 18" displayed on the screen

  Scenario: 45609_Reagent parameter screen(Editing) - "Delete"_"No"
    Given I am on the "popup ID 18"
    When I press "No" in popup
    Then The Reagent is not deleted
    And I am on the "Reagent parameter screen(Editing)" with updated values

  #TBD-  Validation of save softkey involves the versioning of resources
  Scenario: 45609_30326(Save)_Reagent parameter screen(Editing) - "Save" softkey functionality
    Given I am on the "Reagent parameter screen(Editing)"
    And I have the parameters with updated values
    When I press the softkey "Save"
    Then The Reagent is saved with updated values
    And I am on the "Reagent parameter screen(Editing)"

  Scenario: 45609_30320(Discard)_Reagent parameter screen(Editing) - "Discard Changes"_"Yes"
    Given I am on the "Reagent parameter screen(Editing)" with updated values
    And I am on the "popup ID 16"
    When I press "Yes" in the Popup
    Then The updated changes are discarded
    And The old values of the parameters are retained
    And I am on the "Reagent parameter screen(Editing)"

  Scenario: 45609_30323(Delete)_Reagent parameter screen(Editing) - "Delete"_"Yes"
    Given I am on the "Reagent parameter screen(Editing)"
    And I am on the "popup ID 18"
    When I press "Yes" in the Popup
    Then The Reagent is deleted
    And The Reagent is removed from the "List of Reagents" screen

  Scenario: 31675_List of Reagents - Sorting - with one Reagent
    Given I am on the "List of Reagents" screen
    And I have only one Reagent in the list
    Then I should not able to Sort the list

  Scenario: 31675_List of Reagents - Sorting - with more than one Reagent
    Given I am on the "List of Reagents" screen
    And I have more than one Reagent in the list
    Then I should be able to Sort the list