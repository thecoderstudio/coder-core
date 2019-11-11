from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.security import Authenticated, Everyone


class DefaultAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def effective_principals(self, request):
        principals = [Everyone]
        if request.authenticated_userid is not None:
            principals.append('user:{}'.format(request.authenticated_userid))
            principals.append(Authenticated)
        return principals


def get_principals(user_id, request):
    return ("user:{}".format(user_id),)
