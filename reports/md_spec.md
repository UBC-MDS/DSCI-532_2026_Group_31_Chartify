# App Specification

## Job Stories

| #   | Job Story                                                                                                                                                                         | Status      | Notes |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ----- |
| 1   | When I have to market a new song, I want to know which platform it is likely to perform better on so I can focus my resources.                                                    | In Progress |       |
| 2   | When I am writing a new song for Youtube, I want to see the most liked/viewed songs on that platform so I can determine what song features are associated with stream popularity. | In Progress |       |
| 3   | When I am producing a new song, I want to see what song features perform best with specific KPI metrics so I know how to tailor my production process for high performance.       | In Progress |       |

## Component Inventory

| ID          | Type  | Shiny Widget/Renderer | Depends On  | Job Story |
| ----------- | ----- | --------------------- | ----------- | --------- |
| `sample_id` | Input | @shiny.widget         | `sample_id` | #1        |
