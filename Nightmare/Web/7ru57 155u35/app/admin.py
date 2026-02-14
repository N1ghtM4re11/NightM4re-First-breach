from flask import Blueprint, session, abort, render_template

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

FLAG = "N!ghtM4re{jw7_0r_fl45k_1_d0n7_c4r3!!}"

@admin_bp.route("/")
def admin_panel():
    if not session.get("is_admin"):
        abort(403)

    return render_template("admin.html", flag=FLAG)
