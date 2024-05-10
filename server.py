from flwr.common import Context, parameters_to_ndarrays
from flwr.server import Driver, LegacyContext, ServerApp, ServerConfig
from flwr.server.strategy import FedAvg
from flwr.server.workflow import DefaultWorkflow, SecAggPlusWorkflow
from workflow_with_log import SecAggPlusWorkflowWithLogs
import flwr.common.recordset_compat as compat
import numpy
import time

# Define strategy
strategy = FedAvg(
    fraction_fit=1.0,  # Select all available clients
    fraction_evaluate=0.0,  # Disable evaluation
    min_available_clients=5,
)


# Flower ServerApp
app = ServerApp()

@app.main()
def main(driver: Driver, context: Context) -> None:
    # Construct the LegacyContext
    context = LegacyContext(
        state=context.state,
        config=ServerConfig(num_rounds=3),
        strategy=strategy,
    )

    # Create the workflow
    workflow = DefaultWorkflow(
        #fit_workflow=SecAggPlusWorkflowWithLogs(
           # num_shares=3,
          #  reconstruction_threshold=2,
         #   timeout=5,
        #)
         # For real-world applications, use the following code instead
         fit_workflow=SecAggPlusWorkflow(
             num_shares=3,
             reconstruction_threshold=2,
         )
    )

    # Execute
    secagg_start = time.time()
    workflow(driver, context)
    secagg_end = time.time()

    paramsrecord = context.state.parameters_records['parameters']
    parameters = compat.parametersrecord_to_parameters(paramsrecord, True)
    ndarrays = parameters_to_ndarrays(parameters)
    print(ndarrays[0])
    numpy.savetxt("result.txt", ndarrays[0])
    file = open("generate.csv", "a")
    tw = str(secagg_end-secagg_start) +","
    file.write(tw)
    file.close()
