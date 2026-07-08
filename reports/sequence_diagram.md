# Sequence Diagram

## Prediction Flow
```text

User        Browser JS       Flask /predict      ML Model (.pkl)
 |                |                 |                    |
 |--fill inputs-->|                 |                    |
 |--click Run---->|                 |                    |
 |                |--POST /predict->|                    |
 |                |   (JSON body)   |                    |
 |                |                 |--model.predict()-->|
 |                |                 |<--prediction-------|
 |                |<--JSON response-|                    |
 |<--show result--|                 |                    |
```
## Chat Flow
```text

User        Browser JS       Flask /chat       chat_history[]
 |                |                 |                 |
 |--type question>|                 |                 |
 |--press Enter-->|                 |                 |
 |                |--POST /chat---->|                 |
 |                |  { question }   |                 |
 |                |                 |--generate_ans() |
 |                |                 |--append entry-->|
 |                |<--answer + hist-|                 |
 |<--render bubble|                 |                 |
 |                |                 |                 |
 |--ask again---->|                 |                 |
 |                |--POST /chat---->|                 |
 |                |                 |--append entry-->|
 |                |<--answer + hist-|                 |
 |<--render bubble|                 |                 |
```
## Error Flow
```text

User        Browser JS       Flask            Error Handler
 |                |                |                 |
 |--bad input---->|                |                 |
 |                |--POST /predict>|                 |
 |                |                |--missing field->|
 |                |                |<--400 error-----|
 |                |<--{ error }----|                 |
 |<--console.err--|                |                 |
```
