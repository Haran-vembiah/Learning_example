Feature: SRD055 Setup Peripherals - Print and Export
  To verify and validate the Print and Export screen and 'Print and Export' parameters
  verifies:
  1) The menu navigation and "Print and Export" screen header
  2) Display of parameters, its control type and format.
  3) Default value and the list of values of the parameters
  4) validation of the parameters, soft keys and Headers

  Scenario: 36297_User navigation - Setup - Peripherals  - Print and Export
    Given The Peripherals "Print and Export" is available for this Instrument type
    And The user is on the "Menu Tree"
    When The user navigate to the "Print and Export" via Setup->Peripherals-> Print and Export
    Then The Terminal displays the "Print and Export" screen

  Scenario: 36298_Print and Export - Screen header
    Given The user is on the "Print and Export" screen
    And The language of Terminal set as "English"
    Then The Terminal displays the screen header as "Print and Export"

  Scenario Outline: 36298_Print and Export - Tabs verification
    Given The user is on the "Print and Export" screen
    And The language of Terminal set as "English"
    Then The Tab <tab_name> is available on "Print and Export" screen
    Examples:
      | tab_name       |
      | Print Report   |
      | Export data    |
      | Resource check |

  Scenario: 36299_Print Report tab - Navigation
    Given The user is on the "Print and Export" screen
    And The language of Terminal set as "English"
    When The User presses the tab "Print Report"
    Then The Terminal displays "Print Report" tab area


  Scenario Outline: 36299_'Print Report' tab area - parameters - Default values
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label      | default_value   | control_type | state   | order |
      | Category         | PDF File writer | ComboBox     | Enabled | 1     |
      | Storage location | USB stick       | ComboBox     | Enabled | 2     |
      | Paper size       | A4              | ComboBox     | Enabled | 3     |


  Scenario: 36299_'Print Report' tab area - parameters - Connection parameter verification
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The parameter "Category" set as "Compact printer"
    And The language of Terminal set as "English"
    Then The Terminal displays the parameter "Connection"

  Scenario Outline: 36299_'Print Report' tab area - parameters - Default values of category 'Printout'
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The parameter "Category" set as "Printout"
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label | order                              | default_value | state   | control_type |
      | Category    | Printout                           | ComboBox      | Enabled | 1            |
      | Printer     | 1° printer from >List of printers< | List          | Enabled | 2            |
      | Paper size  | A4                                 | ComboBox      | Enabled | 3            |
      | Color mode  | Grayscale                          | ComboBox      | Enabled | 4            |
      | Duplex mode | None                               | ComboBox      | Enabled | 5            |


  Scenario Outline: 36299_'Print Report' tab area - Category - Parameter validation
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "Category"
    Then The Terminal displays the value <value> for the parameter "Category"
    And The User shall able to select the value <value>
    Examples:
      | value           |
      | PDF file writer |
      | Compact printer |
      | Printout        |
      | None            |

  Scenario Outline: 36299_'Print Report' tab area - Storage location - Parameter validation
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The language of Terminal set as "English"
    And The parameter "Category" set as "PDF file writer"
    When The User selects the parameter "Storage location"
    Then The Terminal displays the value <value> for the parameter "Storage location"
    And The User shall able to select the value <value>
    Examples:
      | value     |
      | USB stick |
      | Network   |

  Scenario Outline: 36299_'Print Report' tab area - Paper size - Parameter validation
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The language of Terminal set as "English"
    And The parameter "Category" set as "PDF file writer"
    When The User selects the parameter "Paper size"
    Then The Terminal displays the value <value> for the parameter "Paper size"
    And The User shall able to select the value <value>
    Examples:
      | value  |
      | A4     |
      | Letter |

  Scenario Outline: 36299_'Print Report' tab area - Connection - Parameter validation
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The language of Terminal set as "English"
    And The parameter "Category" set as "Compact printer"
    And The Terminal <Connection_status> with Compact printer
    Then The Terminal displays the value <value> for the parameter "Connection"
    Examples:
      | Connection_status | value         |
      | Not connected     | Not connected |
      | Connected         | TBD           |

  Scenario: 36299_'Print Report' tab area - Printer - Parameter validation
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The language of Terminal set as "English"
    And The parameter "Category" set as "Printout"
    When The User selects the parameter "Printer"
    Then The Terminal displays the "List of printers" screen

  Scenario: 38255_'Print Report' tab area - List of printers screen - Header and softkey verification
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The language of Terminal set as "English"
    And The parameter "Category" set as "Printout"
    When The User selects the parameter "Printer"
    Then The Terminal displays the "List of printers" screen
    And The Terminal displays the screen header as "Select printer"
    And The Softkey "Cancel" is available at position "1"

  Scenario Outline: 38255_'Print Report' tab area - List of printers screen - Column headers verification
    Given The user is on the "Print and Export" screen
    And The user is on "Print Report" tab area
    And The language of Terminal set as "English"
    And The parameter "Category" set as "Printout"
    When The User selects the parameter "Printer"
    Then The Terminal displays the "List of printers" screen
    And The column header <header> is in position <order> from left
    Examples:
      | header   | order |
      | Printer  | 1     |
      | Location | 2     |
      | State    | 3     |

   # TODO: Validation of values for column headers 'Location' and the 'State' are TBD

  Scenario: 38255_'Print Report' tab area - List of printers screen - With only one printer connected
    Given The user is on the "List of printers" screen
    And The user have only one printer in the list
    Then The user should not able to Sort the list

  Scenario: 38255_'Print Report' tab area - List of printers screen - With more than one printer connected
    Given The user is on the "List of printers" screen
    And The user have more than one printer in the list
    Then The user should be able to Sort the list


  Scenario: 36300_Export data tab area - Navigation
    Given The user is on the "Print and Export" screen
    And The language of Terminal set as "English"
    When The User presses the tab "Export data"
    Then The Terminal displays "Export data" tab area

  Scenario Outline: 36300_'Export data' tab area - parameters - Default values
    Given The user is on the "Print and Export" screen
    And The user is on "Export data" tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label | default_value | control_type | state   | order |
      | Export data | None          | ComboBox     | Enabled | 1     |

  Scenario Outline: 36300_Export data tab area - Export data - Parameter validation
    Given The user is on the "Print and Export" screen
    And The user is on "Export data" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "Export data"
    Then The Terminal displays the value <value> for the parameter "Paper size"
    And The User shall able to select the value <value>
    Examples:
      | value |
      | CSV   |
      | None  |

  Scenario: 36300_Export data tab area - Storage location parameter verification
    Given The user is on the "Print and Export" screen
    And The user is on "Export data" tab area
    And The parameter "Export data" set as "CSV"
    And The language of Terminal set as "English"
    Then The Terminal displays the parameter "Storage location"


  Scenario Outline: 36300_Export data tab area - Storage location - Parameter validation
    Given The user is on the "Print and Export" screen
    And The user is on "Export data" tab area
    And The parameter "Export data" set as "CSV"
    And The language of Terminal set as "English"
    When The User selects the parameter "Storage location"
    Then The Terminal displays the value <value> for the parameter "Storage location"
    And The User shall able to select the value <value>
    Examples:
      | value     |
      | USB stick |
      | Network   |

  Scenario: 36301_Resource check tab area - Navigation
    Given The user is on the "Print and Export" screen
    And The language of Terminal set as "English"
    When The User presses the tab "Resource check"
    Then The Terminal displays "Resource check" tab area

  Scenario Outline: 36300_Resource check tab area - parameters - Default values
    Given The user is on the "Print and Export" screen
    And The user is on "Resource check" tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label                         | default_value | control_type | state   | order |
      | Check printer availability and wait | N             | BOOLEAN      | Enabled | 1     |
      | Check USB stick availability        | N             | BOOLEAN      | Enabled | 1     |
      | Check network storage               | N             | BOOLEAN      | Enabled | 1     |

  # TODO: To validate the parameters of Resource check tab area - Behaviour of 'Printer check' parameters requirement is in draft state

  # To verify the visibility of softkeys "Discard" and "Save"
  Scenario Outline: 36298_30327_'Print and Export' screen - Unsaved changes - Softkeys verification
    Given The user is on the "Print and Export" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    When Parameters in <tab_name> tab area has new values
    Then The softkey "Cancel" is visible at position "1"
    And The softkey "Save" is visible at position "5"
    And The User cannot access the other tabs
    Examples:
      | tab_name       |
      | Print Report   |
      | Export data    |
      | Resource check |


  Scenario Outline: 36298_30320(Discard)_'Print and Export' screen- "Discard Changes" popup
    Given The user is on the "Print and Export" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    When The user presses the softkey "Discard"
    Then The Terminal displays the "popup ID 16" on the screen
    Examples:
      | tab_name       |
      | Print Report   |
      | Export data    |
      | Resource check |

  Scenario: 36298_'Print and Export' screen- - "Discard Changes"_"No"
    Given The user is on the "popup ID 16"
    When The user presses "No" in "popup ID 16"
    Then The user is on the "'Print and Export' screen
    And The parameters are with updated values

  Scenario Outline: 36298_30320(Discard)_'Print and Export' screen- "Discard Changes"- Yes
    Given The user is on the "Print and Export" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    And The User cannot access the other tabs
    And The user is on the "popup ID 16"
    When The user presses "Yes" in the "popup ID 16"
    Then The updated changes are discarded
    And The old values of the parameters are retained
    And The user is on <tab_name> tab area
    And The User can able to access the other tabs
    Examples:
      | tab_name       |
      | Print Report   |
      | Export data    |
      | Resource check |

  Scenario Outline: 36298_30326(Save)_'Print and Export' screen - "Save" softkey functionality
    Given The user is on the "Print and Export" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    And The User cannot access the other tabs
    When The user presses the softkey "Save"
    Then The Parameters on <tab_name> tab area is saved with updated values
    And The user is on <tab_name> tab area
    And The User can able to access the other tabs
    Examples:
      | tab_name       |
      | Print Report   |
      | Export data    |
      | Resource check |

