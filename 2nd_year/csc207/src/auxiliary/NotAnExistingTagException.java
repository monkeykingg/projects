package auxiliary;

public class NotAnExistingTagException extends Exception {

	/** A NotPhotoException.*/
	public NotAnExistingTagException() {
		super();
	}

	/**
	 * A NotAnExistingTagException.
	 * 
	 * @param msg
	 *            the message
	 */
	public NotAnExistingTagException(String msg) {
		super(msg);
	}

}
