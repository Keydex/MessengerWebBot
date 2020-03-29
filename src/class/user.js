class User {
  constructor(user_id) {
    this._user = {};
    this._user.user_id = user_id;
    this._user.chatState = 'Initial';
    this._user.websiteData = {};
    this._user.created = new Date().toISOString();
    this._user.modified = new Date().toISOString();
  }

  get user_id() {
    return this._user.user_id;
  }

  get chatState() {
    return this._user.chatState;
  }

  get websiteData() {
    return this._user.websiteData;
  }

  get created() {
    const {created} = this._user;
    return created;
  }

  get modified() {
    const {modified} = this._user;
    return modified;
  }

  set modified(modified) {
    this._user.modified = modified;
  }

  // Change this to get all variables into object
  export() {
    return this._user;
  }

  async update() {
    const originalVersionKey = this._user.modified;
    this._user.modified = new Date().toISOString();
    return userModel.update(this._user, originalVersionKey);
  }
}

module.exports = User;