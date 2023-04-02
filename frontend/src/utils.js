const isArray = Array.isArray;
const isEmpty = obj => [Object, Array].includes((obj || {}).constructor) && !Object.entries((obj || {})).length;

export {isArray, isEmpty}