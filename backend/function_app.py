import azure.functions as func
import auth.register as register
import auth.login as login
import auth.logout as logout
import users.get_profile as get_profile
import users.update_profile as update_profile
import users.update_pref as update_pref
import users.delete_account as delete_account
import admin.get_all_users as get_all_users
import admin.block_user as block_user
import admin.change_role as change_role
import admin.reset_password as reset_password
import admin.get_reports as get_reports
import pokemon.get_pokemon as get_pokemon
import pokemon.search_pokemon as search_pokemon
import favorites.get_favorites as get_favorites
import favorites.add_favorites as add_favorites
import favorites.remove_favorites as remove_favorites
import team.get_team as get_team
import team.add_to_team as add_to_team
import team.remove_from_team as remove_from_team
import team.update_team as update_team

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="auth/register", methods=["POST"])
def auth_register(req: func.HttpRequest) -> func.HttpResponse:
    return register.main(req)

@app.route(route="auth/login", methods=["POST"])
def auth_login(req: func.HttpRequest) -> func.HttpResponse:
    return login.main(req)

@app.route(route="auth/logout", methods=["POST"])
def auth_logout(req: func.HttpRequest) -> func.HttpResponse:
    return logout.main(req)

@app.route(route="users/profile", methods=["GET"])
def users_get_profile(req: func.HttpRequest) -> func.HttpResponse:
    return get_profile.main(req)

@app.route(route="users/profile", methods=["PUT"])
def users_update_profile(req: func.HttpRequest) -> func.HttpResponse:
    return update_profile.main(req)

@app.route(route="users/preferences", methods=["PUT"])
def users_update_pref(req: func.HttpRequest) -> func.HttpResponse:
    return update_pref.main(req)

@app.route(route="users/account", methods=["DELETE"])
def users_delete_account(req: func.HttpRequest) -> func.HttpResponse:
    return delete_account.main(req)

@app.route(route="mgmt/users", methods=["GET"])
def admin_get_all_users(req: func.HttpRequest) -> func.HttpResponse:
    return get_all_users.main(req)

@app.route(route="mgmt/block", methods=["PUT"])
def admin_block_user(req: func.HttpRequest) -> func.HttpResponse:
    return block_user.main(req)

@app.route(route="mgmt/role", methods=["PUT"])
def admin_change_role(req: func.HttpRequest) -> func.HttpResponse:
    return change_role.main(req)

@app.route(route="mgmt/reset-password", methods=["PUT"])
def admin_reset_password(req: func.HttpRequest) -> func.HttpResponse:
    return reset_password.main(req)

@app.route(route="mgmt/reports", methods=["GET"])
def admin_get_reports(req: func.HttpRequest) -> func.HttpResponse:
    return get_reports.main(req)

@app.route(route="pokemon/search", methods=["GET"])
def pokemon_search(req: func.HttpRequest) -> func.HttpResponse:
    return search_pokemon.main(req)

@app.route(route="pokemon/{name_or_id}", methods=["GET"])
def pokemon_get(req: func.HttpRequest) -> func.HttpResponse:
    return get_pokemon.main(req)

@app.route(route="favorites", methods=["GET"])
def favorites_get(req: func.HttpRequest) -> func.HttpResponse:
    return get_favorites.main(req)

@app.route(route="favorites", methods=["POST"])
def favorites_add(req: func.HttpRequest) -> func.HttpResponse:
    return add_favorites.main(req)

@app.route(route="favorites/{pokemon_id}", methods=["DELETE"])
def favorites_remove(req: func.HttpRequest) -> func.HttpResponse:
    return remove_favorites.main(req)

@app.route(route="team", methods=["GET"])
def team_get(req: func.HttpRequest) -> func.HttpResponse:
    return get_team.main(req)

@app.route(route="team", methods=["POST"])
def team_add(req: func.HttpRequest) -> func.HttpResponse:
    return add_to_team.main(req)

@app.route(route="team", methods=["PUT"])
def team_update(req: func.HttpRequest) -> func.HttpResponse:
    return update_team.main(req)

@app.route(route="team/{pokemon_id}", methods=["DELETE"])
def team_remove(req: func.HttpRequest) -> func.HttpResponse:
    return remove_from_team.main(req)