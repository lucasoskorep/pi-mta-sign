/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * An enumeration.
 * @export
 * @interface Route
 */
export interface Route {
}

/**
 * Check if a given object implements the Route interface.
 */
export function instanceOfRoute(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function RouteFromJSON(json: any): Route {
    return RouteFromJSONTyped(json, false);
}

export function RouteFromJSONTyped(json: any, ignoreDiscriminator: boolean): Route {
    return json;
}

export function RouteToJSON(value?: Route | null): any {
    return value;
}

