exports.setError = (path, message) => {
  const errorObj = {path, message};
  console.log('Generating error', errorObj);
  return errorObj;
};