const isArray = Array.isArray;
const isEmpty = obj => [Object, Array].includes((obj || {}).constructor) && !Object.entries((obj || {})).length;
const find = function(arr, obj) {
  return arr.find((elem) => {
    return obj && Object.keys(obj).every(key => elem[key] === obj[key]);
  }) || arr[0];
}

export {isArray, isEmpty, find}