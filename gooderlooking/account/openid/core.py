# -*- coding: utf-8 -*-
from flask import current_app, Blueprint, redirect, request, session
from flask.ext.security import (AuthenticationProvider, exceptions)


class OpenIDAuthenticationProvider(AuthenticationProvider):
    """Implementation of flask.ext.security.AuthenticationProvider to support
    OpenID authentication.

    :param login_form_class: The login form class to use when authenticating a
                             user
    """
    

    def authenticate_openid(self, token):
        """Processes an OpenID session token and returns a user instance if
        authentication is successful.

        :param form: An instance of a populated login form
        """
        return self.do_authenticate_openid(token)

    def do_authenticate_openid(self, token):
        """Returns the authenticated user if authentication is successfull. If
        authentication fails an appropriate error is raised

        :param token: The OpenID session token
        """
        try:
            user = current_app.security.datastore.find_user(openid=session['openid'])
        except AttributeError, e:
            self.auth_error("Could not find user datastore: %s" % e)
        except exceptions.UserNotFoundError, e:
            raise exceptions.BadCredentialsError("Specified user does not exist")
        except Exception, e:
            self.auth_error('Unexpected authentication error: %s' % e)
            
        return user