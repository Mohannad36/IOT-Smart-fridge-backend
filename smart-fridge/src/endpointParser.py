import json

from utils import stringToClassUsingModule

def parseEndpoints(endpointsConfigPath: str) -> dict:
    outData: dict = {}
    baseUrl: str = None
    with open(endpointsConfigPath) as config:
        data = json.load(config)
        base: str = None

        baseEndpointUrl: str = None

        endpointUrl: str = None
        endpointAction: str = None

        endpointsSection: str = None
        for key in data:
            base = data[key]
            baseUrl = key
            for section in base:
                sectionName = next(iter(section.keys()))
                base = section[sectionName]

                baseRouteUrl = base["baseRoute"]

                endpointUrl = baseUrl + baseRouteUrl
                endpointAction = base["action"]

                constructKeyPair(outData, endpointUrl, endpointAction)

                subRoutes = base["subRoutes"]
                subRouteUrl = None
                for route in subRoutes:
                    subRouteUrl = next(iter(route.keys()))
                    endpointUrl = baseRouteUrl + subRouteUrl #baseUrl + baseRouteUrl + subRouteUrl
                    endpointAction = stringToClassUsingModule(route[subRouteUrl]["action"], "services.restless.routing.routeActions")
                    constructKeyPair(outData, endpointUrl, endpointAction)
    return outData

def constructKeyPair(endpoints: dict, endpointUrl: str, endpointAction: str):
    endpoints[endpointUrl] = endpointAction

def main() -> None:
    pass

if __name__ == "__main__":
    main()
