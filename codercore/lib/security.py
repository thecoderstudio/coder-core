from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.security import Authenticated, Everyone


class DefaultAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def effective_principlas(self, request):
        principals = [Everyone]
        if request.user is not None:
            principals.append('user:{}'.format(request.user.id))
            principals.append(Authenticated)
        return principals


def get_principals(user_id, request):
    return ("user:{}".format(user_id),)
