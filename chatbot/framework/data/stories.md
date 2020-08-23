## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge {"protocol_name":"HyperBusSpecification"}
  - slot {"protocol_name":"HyperBusSpecification"}
  - action_faq_qa_model

## bot challenge
* bot_challenge {"protocol_name":"I2C"}
  - slot {"protocol_name":"I2C"}
  - action_faq_qa_model