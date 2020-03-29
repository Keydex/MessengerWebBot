class User {
  constructor(userObj) {
    const {user_id, chatState, websiteData, created, modified} = userObj;
    this._user.user_id = user_id;
    this._user.chatState = chatState || 'Initial';
    this._user.websiteData = websiteData || {};
    this._user.created = created || new Date().toISOString();
    this._user.modified = modified || new Date().toISOString();
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

  export() {
    return this._user;
  }

  async update() {
    const originalVersionKey = this._user.modified;
    this._user.modified = new Date().toISOString();
    return userModel.update(this._user, originalVersionKey);
  }
}
