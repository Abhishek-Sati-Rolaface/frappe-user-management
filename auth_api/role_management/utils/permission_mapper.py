
LINKED_DOCTYPE_PERMISSION_MAP = {
    "Customer": ["Address", "Contact"],
}




def expand_with_linked_permissions(permissions: list) -> list:
    """
    For each permission in the list, check if its module has linked doctypes.
    If so, auto-generate permission entries for those linked doctypes
    inheriting ALL ptypes from the root permission.

    Already-present linked doctypes in the payload are NOT overwritten.

    """
    explicit_modules   = {p["module"] for p in permissions}
    linked_permissions = []

    for permission in permissions:
        module          = permission["module"]
        linked_doctypes = LINKED_DOCTYPE_PERMISSION_MAP.get(module)

        if not linked_doctypes:
            continue

        # ── Inherit everything except the module key itself ───────────────────
        inherited_ptype_map = {k: v for k, v in permission.items() if k != "module"}

        if not inherited_ptype_map:
            continue

        for linked_doctype in linked_doctypes:
            # ── Skip if already explicitly defined in payload ─────────────────
            if linked_doctype in explicit_modules:
                continue

            linked_permissions.append({
                "module": linked_doctype,
                **inherited_ptype_map,
            })

            # Prevent duplicates if multiple roots share the same linked doctype
            explicit_modules.add(linked_doctype)

    return permissions + linked_permissions