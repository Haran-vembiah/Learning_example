Feature: SRD077 Setup Blank values
  To verify and validate the List of Burettes screen and Burette parameters
  verifies:
  1) The menu navigation and "List of burette" screen header and column header
  2) Display of parameters, its control type and format.
  3) Default value and the list of values of the parameters
  4) validation of the parameters, soft keys and Headers

  Scenario: 45607_User navigation - Setup - Values & Tables - Blank Values
    Given I am on the "Menu Tree"
    When I navigate to the "Blank values" via Setup->Values & Tables
    Then The "List of blank values" screen is displayed

  Scenario: 45608_List of blank values - Screen header
    Given I am on the "List of blank values" screen
    Then The screen header is displayed as "Blank values"

  Scenario Outline: 45608_List of blank values - column headers
    Given I am on the "List of blank values" screen
    Then The column header <header> is in position <order> from left
    Examples:
      | header | order |
      | Name   | 1     |
      | Value  | 2     |

  Scenario: 45608_List of blank values - Display of "New" softkey
    Given I am on the "List of blank values" screen
    Then The softkey "New" is displayed at position "3"

  Scenario: 45608_List of blank values - "New" softkey functionality
    Given I am on the "List of blank values" screen
    When I press the softkey "New"
    Then I am on the "Blank values parameters(Creation)" screen

  Scenario: 45609_46374_Blank value parameter screen(Creation) - screen Header
    Given I am on the "Blank value Parameter(Creation)" screen
    Then The screen header is displayed as "Blank Value"

  Scenario Outline: 45609_Blank value parameter screen(Creation) - softkeys verification
    Given I am on the "Blank value Parameter(Creation)" screen
    Then The softkey <softkey> is visible
    #TODO: Not implemented for color verification
    And The softkey <softkey> is in <color>
    And The softkey <softkey> is at position <position>
    Examples:
      | softkey | color | position |
      | Cancel  | Blue  | 1        |
      | Create  | Green | 5        |

  Scenario: 45609_30321(Cancel)Navigation to Blank values list screen from parameter screen
    Given I am on the "Blank value Parameter(Creation)" screen
    When I press the softkey "Cancel"
    Then I am on the "List of blank values" screen

  Scenario Outline: 45609_46374_Blank value parameter screen(Creation) - parameters - Default values - 'Blank value' tab area
    Given I am on the "Blank value Parameter(Creation)" screen
    And I am on "Blank value" tab area
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
  Scenario Outline: 45609_46374_Blank value parameter screen(Creation) - parameters - Default values - 'Monitoring' tab area
    Given I am on the "Blank value Parameter(Creation)" screen
    And I am on "Monitoring" tab area
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label | default_value | control_type | state | order |

  # Parameters in this tab are more related to LCM and HR
  Scenario Outline: 45609_46374_Blank value parameter screen(Creation) - parameters - Default values - 'General' tab area
    Given I am on the "Blank value Parameter(Creation)" screen
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


  Scenario Outline: 45609_Blank value parameter screen(Creation) - Name - parameter validation
    Given I am on the "Blank value Parameter(Creation)" screen
    And I am on "Blank value" tab area
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
  Scenario: 45609_Blank value parameter screen(Creation) - ID - parameter validation
    Given I am on the "Blank value Parameter(Creation)" screen
    And I am on "Blank value" tab area
    Then The parameter ID has the value "Value x"

  Scenario Outline: 45609_Blank value parameter screen(Creation) - Unit - parameter validation
    Given I am on the "Blank value Parameter(Creation)" screen
    And I am on "Blank value" tab area
    And I am on the keyboard screen displayed for the parameter "Unit"
    When I enter the value <input>
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    Examples:
      | input              | accept_reject | validation_msg       |
      | mmmol              | Accepts       | No                   |
      | BlanknameBlankname | Rejects       | Value outside limits |
      | mol                | Accepts       | No                   |

  Scenario Outline: 45609_Blank value parameter screen(Creation) - Value - parameter validation
    Given I am on the "Blank value Parameter(Creation)" screen
    And I am on "Blank value" tab area
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
  Scenario: 45609_Blank value parameter screen(Creation) - Determination method - parameter validation
    Given I am on the "Blank value Parameter(Creation)" screen
    And I am on "Blank value" tab area
    # TBD the value
    Then The value of the parameter "Determination method" should be Value

  # Validation of this parameter involves on various other resources defined in multiple SRDs
  Scenario: 45609_Blank value parameter screen(Creation) - Determination date - parameter validation
    Given I am on the "Blank value Parameter(Creation)" screen
    And I am on "Blank value" tab area
    # TBD the value
    Then The value of the parameter "Determination date" should be Value

  # Validation of this parameter involves on various other resources defined in multiple SRDs
  Scenario: 45609_Blank value parameter screen(Creation) - Determined by - parameter validation
    Given I am on the "Blank value Parameter(Creation)" screen
    And I am on "Blank value" tab area
    # TBD the value
    Then The value of the parameter "Determined by" should be Logged-in user

  # Validation of parameters in "Monitoring" tab area - TBD

  # Parameters in the "General" tab area are related to LCM

  Scenario: 45609_30325(Create)_Blank value parameter screen(Creation) - "Create" softkey functionality
    Given I am on the "Blank value Parameter(Creation)" screen
    And All the parameters has valid values
    When I press the softkey "Create"
    Then The new "Blank value" is created
    And The "Blank value parameter screen(Editing)" screen is displayed

  Scenario Outline: 45609_Blank value parameter screen(Editing) - softkeys verification
    Given I am on the "Blank value parameter screen(Editing)" screen
    Then The softkey <softkey> is visible
    And The softkey <softkey> is in <color>
    And The softkey <softkey> is at position <position>
    Examples:
      | softkey | color | position |
      | Back    | Blue  | 1        |
      | Delete  | Blue  | 3        |

  Scenario: 45609_30322(Back)Navigation to Blank values list screen from parameter screen
    Given I am on the "Blank value Parameter(Editing)" screen
    When I press the softkey "Cancel"
    Then I am on the "List of blank values" screen

  Scenario: 45608_List of Blank values - Selection of existing blank value
    Given I am on the "List of blank values" screen
    When I select any Blank value from the list
    Then I am on the "Blank value parameter screen(Editing)" screen

  Scenario Outline: 45609_46374_Blank value parameter screen(Editing) - unsaved changes - sofktkeys verification
    Given I am on the "Blank value parameter screen(Editing)" screen
    When I update any parameter of blank value with new value
    Then The softkey <softkey> is visible
    And The softkey <softkey> is in <color>
    And The softkey <softkey> is at position <position>
    Examples:
      | softkey | color | position |
      | Discard | Blue  | 1        |
      | Delete  | Blue  | 3        |
      | Save    | Green | 5        |

  Scenario: 45609_30320(Discard)_Blank value parameter screen(Editing)- "Discard Changes" popup
    Given I am on the "Blank value parameter screen(Editing)" screen with updated values
    When I press the softkey "Discard"
    Then The "popup ID 16" displayed on the screen

  Scenario: 45609_Blank value parameter screen(Editing) - "Discard Changes"_"No"
    Given I am on the "popup ID 16"
    When I press "No" in popup
    Then I am on the "Blank value parameter screen(Editing)" screen
    And I have the parameters with updated values

  Scenario: 45609_30323(Delete)_Blank value parameter screen(Editing) - "Delete" popup
    Given I am on the "Blank value parameter screen(Editing)" with updated values
    When I press the softkey "Delete"
    Then The "popup ID 18" displayed on the screen

  Scenario: 45609_Blank value parameter screen(Editing) - "Delete"_"No"
    Given I am on the "popup ID 18"
    When I press "No" in popup
    Then The Blank value is not deleted
    And I am on the "Blank value parameter screen(Editing)" with updated values

  #TBD-  Validation of save softkey involves the versioning of resources
  Scenario: 45609_30326(Save)_Blank value parameter screen(Editing) - "Save" softkey functionality
    Given I am on the "Blank value parameter screen(Editing)"
    And I have the parameters with updated values
    When I press the softkey "Save"
    Then The Blank value is saved with updated values
    And I am on the "Blank value parameter screen(Editing)"

  Scenario: 45609_30320(Discard)_Blank value parameter screen(Editing) - "Discard Changes"_"Yes"
    Given I am on the "Blank value parameter screen(Editing)" with updated values
    And I am on the "popup ID 16"
    When I press "Yes" in the Popup
    Then The updated changes are discarded
    And The old values of the parameters are retained
    And I am on the "Blank value parameter screen(Editing)"

  Scenario: 45609_30323(Delete)_Blank value parameter screen(Editing) - "Delete"_"Yes"
    Given I am on the "Blank value parameter screen(Editing)"
    And I am on the "popup ID 18"
    When I press "Yes" in the Popup
    Then The Blank value is deleted
    And The Blank value is removed from the "List of Blank values" screen

  Scenario: 45608_List of Blank values - Sorting - with one Blank value
    Given I am on the "List of blank values" screen
    And I have only one Blank value in the list
    Then I should not able to Sort the list

  Scenario: 45608_List of Blank values - Sorting - with more than one blank value
    Given I am on the "List of blank values" screen
    And I have more than one Blank value in the list
    Then I should be able to Sort the list