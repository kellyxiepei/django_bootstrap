from shared.auth.wechat.support_wechat_mini import UnionIdUserStoreBase


class DemoUnionIdUser():
    def __init__(self, union_id):
        self._union_id = union_id


class UnionIdUserStoreDemo(UnionIdUserStoreBase):
    def get_user_by_union_id(self, union_id):
        return DemoUnionIdUser(union_id)
