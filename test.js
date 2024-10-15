const str = "Hello    world!   How  are   you?";
// Thay thế tất cả các chuỗi khoảng trắng bằng một khoảng trắng
const result = str.replace(/\s+/g, ' ');
console.log(result);  // Output: "Hello  world!  How are  you?"
