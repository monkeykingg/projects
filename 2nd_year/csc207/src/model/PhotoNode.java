package model;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import javafx.util.Pair;

import auxiliary.CannotUndoNameException;
import auxiliary.DuplicateTagException;
import auxiliary.NotAnExistingTagException;

/**
 * A node, which represents a photo.
 */
public class PhotoNode extends FileNode {

	/** A calendar for PhotoNode to keep track of time. */
	private static Calendar calendar = Calendar.getInstance();

	/**
	 * The current PhotoName for the node, which keeps track of both the string
	 * representation of photo name and corresponding tags shown in the string
	 * representation of photo name.
	 */
	private PhotoName currPhotoName;

	/**
	 * The string of the plain name, i.e. without tags and extension, of a photo
	 * node. Since we only rename a photo by adding or removing tags, then the
	 * plain name of a photo node will not change when we are only using the
	 * photo renamer.
	 */
	private String plainName;

	/**
	 * The string representation of the extension (including the "." as a
	 * separator at the beginning) in the name of a photo node. Since we only
	 * rename a photo by adding or removing tags, then the extension of a photo
	 * node will not change when we are only using the photo renamer.
	 */
	private String extension;

	/**
	 * The list of 2-element pair for (specific time, corresponding PhotoName),
	 * which keeps track of all names a photo node ever had in accordance with
	 * the time line and the corresponding time those names were generated to be
	 * the name of the node.
	 */
	private ArrayList<Pair<Date, PhotoName>> allNames;

	/**
	 * A node, which represents a photo.
	 *
	 * @param name
	 *            the string of the current name of the PhotoNode
	 * @param parent
	 *            the PhotoNode's parent node, which represents the directory
	 *            containing this photo
	 */
	public PhotoNode(String name, FileNode parent) {
		// PhotoNode has a FileNode part. Call super's constructor.
		super(name, parent, FileType.IMAGE);

		// Initialize other instance variables.
		currPhotoName = new PhotoName(name);
		plainName = PhotoName.extractPlainNameWithoutTags(name);
		extension = PhotoName.extractExtension(name);
		allNames = new ArrayList<Pair<Date, PhotoName>>();
		allNames.add(new Pair<Date, PhotoName>(calendar.getTime(), currPhotoName));
	}

	/**
	 * Return current PhotoName for this PhotoNode.
	 * 
	 * @return the currPhotoName
	 */
	public PhotoName getCurrPhotoName() {
		return currPhotoName;
	}

	/**
	 * Return the string of the plain name, i.e. without tags and extension, of
	 * this PhotoNode.
	 * 
	 * @return the plainName
	 */
	public String getPlainName() {
		return plainName;
	}

	/**
	 * Return the string representation of the extension (including the "." as a
	 * separator at the beginning) in the name of this PhotoNode.
	 * 
	 * @return the extension
	 */
	public String getExtension() {
		return extension;
	}

	/**
	 * Return the list of 2-element pair for (specific time, corresponding
	 * PhotoName), which keeps track of all names a photo node ever had in
	 * accordance with the time line and the corresponding time those names were
	 * generated to be the name of the node.
	 * 
	 * @return the allNames
	 */
	public ArrayList<Pair<Date, PhotoName>> getAllNames() {
		return allNames;
	}

	/**
	 * Revert the name of the photo node back to an older name oldName if
	 * oldName is an existing past name for the photo node. If there were
	 * several oldName existing as past names, revert to the latest one.
	 *
	 * @param oldName
	 *            the older PhotoName to revert back to if possible
	 * @throws CannotUndoNameException
	 */
	public void backToOlderName(PhotoName oldName) throws CannotUndoNameException {
		// If we do have past names other than the current one, we can check the
		// possibility of going back to oldName.
		// Otherwise, directly throw an exception.
		if (allNames.size() <= 1) {

			String msg = "CAN'T UNDO: Not any past name existing!";
			throw new CannotUndoNameException(msg);
		} else {

			// Loop over the list of all past names existing before current one.
			for (int i = allNames.size() - 2; i >= 0; i--) {

				// Get the current PhotoName we're looking at and do the
				// comparison with oldName.
				PhotoName curr = allNames.get(i).getValue();
				if (curr.equals(oldName)) {

					// If we do find oldName as an existing past name,
					// we can revert back and then stop.
					int times = allNames.size() - i - 1;
					for (int j = 1; j <= times; j++) {
						allNames.remove(allNames.size() - 1);
					}
					currPhotoName = allNames.get(allNames.size() - 1).getValue();

					// Update name as a FileNode
					this.setName(currPhotoName.getStrPhotoName());

					return;
				}
			}

			// If oldName is not an existing past name, throw an exception.
			String msg = "CAN'T UNDO: " + oldName.toString() + " is not an existing past name!";
			throw new CannotUndoNameException(msg);
		}
	}

	/**
	 * Revert the name of the photo node back to the closest state merely before
	 * a particular time date if there were past names existed before that date
	 * for the photo node. If the first name for the node was generated after
	 * that date, revert back to the first name of the node.
	 *
	 * @param date
	 *            the time to revert back to
	 */
	public void backToDate(Date date) {
		// If we do have past names other than the current one, we can revert
		// back. Otherwise, leave the name as the current one and don't do any
		// further modification.
		if (allNames.size() > 1) {

			// Record the index of the past name to revert back to in allNames.
			Integer index;
			for (index = allNames.size() - 1; index >= 0; index--) {
				if (allNames.get(index).getKey().before(date)) {
					break;
				}
			}

			// Do the reverting for the allNames
			if (index > 0) {
				ArrayList<Pair<Date, PhotoName>> acc = new ArrayList<Pair<Date, PhotoName>>();
				for (int i = 0; i <= index; i++) {
					acc.add(allNames.get(i));
				}
				allNames = acc;
			} else {
				Pair<Date, PhotoName> firstName = allNames.get(0);
				allNames = new ArrayList<Pair<Date, PhotoName>>();
				allNames.add(firstName);
			}

			// Set the current PhotoName.
			currPhotoName = allNames.get(allNames.size() - 1).getValue();

			// Update name as a FileNode
			this.setName(currPhotoName.getStrPhotoName());
		}
	}

	/**
	 * Revert the name of the photo node back to the latest name before current
	 * name if there exists a past name.
	 *
	 * @throws CannotUndoNameException
	 */
	public void undoPhotoName() throws CannotUndoNameException {
		// Check if the photo node ever had any name before the current one.
		if (allNames.size() <= 1) {

			// If not any past names existing before the current one, can't undo
			// name, and throw an exception.
			String msg = "CAN'T UNDO: No past names before the current one: " + currPhotoName.toString();
			throw new CannotUndoNameException(msg);
		} else {

			// If here's at least one past name, undo name.
			allNames.remove(allNames.size() - 1);
			currPhotoName = allNames.get(allNames.size() - 1).getValue();

			// Update name as a FileNode
			this.setName(currPhotoName.getStrPhotoName());
		}
	}

	/**
	 * Update a new PhotoName for the PhotoNode based on the new string
	 * representation newStrName.
	 * 
	 * @param newStrName
	 *            the string representation of the new name
	 */
	private void updatePhotoName(String newStrName) {
		// Update name as a FileNode
		this.setName(newStrName);

		// Generate a new PhotoName and update current PhotoName for the
		// photo node. Record the time.
		PhotoName newPhotoName = new PhotoName(newStrName);
		currPhotoName = newPhotoName;
		Date current = calendar.getTime();

		// Update allNames by including the new name.
		allNames.add(new Pair<Date, PhotoName>(current, newPhotoName));
	}

	/**
	 * Rename the photo node by adding a new tag. Can't add the same tag twice
	 * for one node.
	 *
	 * @param newTag
	 *            the new tag to add
	 * @throws DuplicateTagException
	 */
	public void tagPhoto(Tag newTag) throws DuplicateTagException {
		// Avoid adding duplicate tags.
		if (!currPhotoName.getLstPhotoTags().contains(newTag)) {

			// Generate a string for the new name and update current PhotoName.
			String nameWithoutExtension = PhotoName.extractNameWithoutExtension(currPhotoName.getStrPhotoName());
			String newStrName = nameWithoutExtension + Tag.getTagSeparator() + newTag.toString() + extension;
			updatePhotoName(newStrName);
		} else {

			String msg = " Cannot add a duplicate tag! " + newTag.toString() + " is already a tag for the photo.";
			throw new DuplicateTagException(msg);
		}
	}

	/**
	 * Rename the photo node by adding several new tags from a list of tags.
	 * Can't add the same tag twice for one node.
	 * 
	 * @param tagsToAdd
	 *            a list of tags to add to the name of the node
	 * @throws DuplicateTagException
	 */
	public void tagPhotoByCollection(ArrayList<Tag> tagsToAdd) throws DuplicateTagException {
		// Keep track of info corresponding to the original name before adding
		// tags.
		ArrayList<Tag> originalTags = currPhotoName.getLstPhotoTags();
		String nameWithoutExtension = PhotoName.extractNameWithoutExtension(currPhotoName.getStrPhotoName());
		String newStrName = nameWithoutExtension;

		// Loop over all new tags want to add to the name.
		for (Tag tag : tagsToAdd) {

			// Avoid adding duplicate tags.
			if (!originalTags.contains(tag)) {

				// Update the newStrName.
				newStrName += Tag.getTagSeparator() + tag.toString();

			} else {

				String msg = " Cannot add a duplicate tag! " + tag.toString() + " is already a tag for the photo.";
				throw new DuplicateTagException(msg);
			}
		}

		// If no exception was thrown, update the name of this node.
		newStrName += extension;
		updatePhotoName(newStrName);
	}

	/**
	 * Rename the photo node by deleting a specific tag of this photo node if
	 * that specified unwantedTag is an existing tag in the current name of the
	 * node.
	 *
	 * @param unwantedTag
	 *            the tag to delete
	 * @throws NotAnExistingTagException
	 */
	public void detagPhoto(Tag unwantedTag) throws NotAnExistingTagException {
		String tagStr = unwantedTag.toString();

		// If unwantedTag is not an existing tag in the current name, throw an
		// exception.
		if (currPhotoName.getStrPhotoName().indexOf(tagStr) == -1) {

			String msg = tagStr + " is not a tag for this photo!";
			throw new NotAnExistingTagException(msg);
		} else {

			// Generate a string for the new name by removing the unwanted tag.
			String newStrName = plainName;
			for (Tag t : currPhotoName.getLstPhotoTags()) {

				// When adding tags, we don't allow add duplicate tags.
				// Thus we can make sure that all tags are distinct.
				if (!t.equals(unwantedTag)) {
					newStrName += Tag.getTagSeparator() + t.toString();
				}
			}
			newStrName += extension;

			// Update currPhotoName.
			updatePhotoName(newStrName);
		}
	}

	/**
	 * Rename the photo node by deleting a list of tags of this photo node if
	 * those tags to remove are all existing tags in the current name of the
	 * node.
	 * 
	 * @param tagsToRemove
	 *            a list of tags to remove from the current name of the node
	 * @throws NotAnExistingTagException
	 */
	public void detagPhotoByCollection(ArrayList<Tag> tagsToRemove) throws NotAnExistingTagException {
		// Keep track of info corresponding to the original name before adding
		// tags.
		ArrayList<Tag> originalTags = currPhotoName.getLstPhotoTags();

		// Construct an accumulator for tags in the renamed name after removal
		// of tags.
		ArrayList<Tag> newTags = new ArrayList<Tag>();
		for (Tag t : originalTags) {
			newTags.add(t);
		}
		String newStrName = plainName;

		for (Tag tag : tagsToRemove) {

			// If tag is not an existing tag in the current name, throw an
			// exception.
			if (!newTags.remove(tag)) {

				String msg = tag.toString() + " is not a tag for this photo!";
				throw new NotAnExistingTagException(msg);
			}
		}

		// If no exception was thrown, update currPhotoName.
		newStrName += PhotoName.combineTags(newTags) + extension;
		updatePhotoName(newStrName);
	}
}
