/** @flectra-module **/

import { FlectraEditor } from "@web_editor/js/editor/flectra-editor/src/FlectraEditor";
import { patch } from "@web/core/utils/patch";

/**
 * The goal of this patch is to remove the crop and replace buttons
 * from the image editor toolbar as the portal user doesn't have
 * access to save modified attachments.
 */
patch(FlectraEditor.prototype, {
    /**
     * @override
     */
    _updateToolbar(show) {
        super._updateToolbar(show);
        const isInMedia = this.toolbar.classList.contains('oe-media');
        const cropButton = this.toolbar.querySelector('#image-crop');
        const replaceButton = this.toolbar.querySelector('#media-replace');
        cropButton?.classList.toggle('d-none', isInMedia);
        replaceButton?.classList.toggle('d-none', isInMedia);
    },
});
